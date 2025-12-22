


import os
import io
import time
import tempfile
import threading
from typing import Optional, Dict, Any, List

import boto3
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from pydantic import BaseModel
from PIL import Image
from ultralytics import YOLO


# ----------------------------
# Config (env 기반)
# ----------------------------
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://127.0.0.1:9000")
S3_BUCKET = os.getenv("S3_BUCKET", "mlflow")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "oracle")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "oracleoracle")
S3_REGION = os.getenv("S3_REGION", "us-east-1")

# 학습 코드와 동일한 규칙:
# key = f"{s3_prefix}/{experiment}/{run_id}/weights/best.pt"
S3_PREFIX = os.getenv("S3_PREFIX", "yolo-artifacts")
EXPERIMENT = os.getenv("EXPERIMENT", "haerujil-yolo")
RUN_ID = os.getenv("RUN_ID", "")  # 필수(또는 MODEL_KEY를 직접 지정)
MODEL_KEY = os.getenv("MODEL_KEY", "")  # 있으면 이걸 우선 사용

# 로컬에 저장될 모델 경로
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", os.path.join(tempfile.gettempdir(), "best.pt"))

# YOLO runtime
DEFAULT_DEVICE = os.getenv("YOLO_DEVICE", "auto")  # "0" / "cpu" / "auto"


# ----------------------------
# Response Schemas
# ----------------------------
class Box(BaseModel):
    cls: int
    conf: float
    xyxy: List[float]  # [x1, y1, x2, y2]


class PredictResponse(BaseModel):
    model_key: str
    local_model_path: str
    image_size: List[int]  # [w, h]
    boxes: List[Box]
    names: Optional[Dict[str, str]] = None
    latency_ms: float


# ----------------------------
# S3 helpers
# ----------------------------
def make_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION,
    )


def resolve_model_key(run_id: str) -> str:
    # MODEL_KEY가 지정되면 그대로 사용
    if MODEL_KEY:
        return MODEL_KEY
    if not run_id:
        raise ValueError("RUN_ID is empty. Set env RUN_ID or env MODEL_KEY.")
    return f"{S3_PREFIX}/{EXPERIMENT}/{run_id}/weights/best.pt"


def download_model_from_s3(key: str, dest_path: str) -> None:
    s3 = make_s3_client()
    # dest 디렉토리 보장
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    s3.download_file(S3_BUCKET, key, dest_path)


# ----------------------------
# Model holder (핫스왑 안전)
# ----------------------------
app = FastAPI(title="YOLO MinIO Serving")

_model_lock = threading.RLock()
_model: Optional[YOLO] = None
_model_key_loaded: str = ""
_model_loaded_at: float = 0.0


def load_yolo_from_local(path: str) -> YOLO:
    # 서버 시작 시 1회 로딩 (요청마다 로딩 금지)
    return YOLO(path)


def current_model_info() -> Dict[str, Any]:
    return {
        "s3_endpoint": S3_ENDPOINT,
        "bucket": S3_BUCKET,
        "model_key_loaded": _model_key_loaded,
        "local_model_path": LOCAL_MODEL_PATH,
        "loaded": _model is not None,
        "loaded_at_epoch": _model_loaded_at,
        "experiment": EXPERIMENT,
        "prefix": S3_PREFIX,
        "default_device": DEFAULT_DEVICE,
    }


def reload_model(run_id: str = "") -> Dict[str, Any]:
    """
    1) S3에서 best.pt 다운로드
    2) YOLO 로드
    3) lock 잡고 글로벌 모델 교체
    """
    global _model, _model_key_loaded, _model_loaded_at

    key = resolve_model_key(run_id or RUN_ID)

    # 임시 파일에 먼저 다운로드 → 로드 성공하면 원자적으로 교체
    tmp_path = LOCAL_MODEL_PATH + ".tmp"
    download_model_from_s3(key, tmp_path)

    new_model = load_yolo_from_local(tmp_path)

    with _model_lock:
        # 기존 파일 교체
        os.replace(tmp_path, LOCAL_MODEL_PATH)
        _model = new_model
        _model_key_loaded = key
        _model_loaded_at = time.time()

    return current_model_info()


@app.on_event("startup")
def on_startup():
    # 서버 시작 시 자동 로드
    reload_model(run_id=RUN_ID)


# ----------------------------
# Endpoints
# ----------------------------
@app.get("/health")
def health():
    return {"status": "ok", **current_model_info()}


@app.post("/reload")
def reload_endpoint(
    run_id: str = Query("", description="학습 run_id (비우면 env RUN_ID 사용)"),
):
    try:
        info = reload_model(run_id=run_id)
        return {"status": "reloaded", **info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(...),
    conf: float = Query(0.25, ge=0.0, le=1.0),
    iou: float = Query(0.5, ge=0.0, le=1.0),
    imgsz: int = Query(640, ge=64, le=4096),
    device: str = Query(DEFAULT_DEVICE, description='"0" / "cpu" / "auto"'),
    max_det: int = Query(300, ge=1, le=3000),
):
    with _model_lock:
        if _model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        model = _model
        model_key = _model_key_loaded

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        img = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    w, h = img.size

    # ultralytics는 device=None이면 자동 선택 동작(환경에 따라)
    dev = None if device == "auto" else device

    t0 = time.perf_counter()
    results = model.predict(
        source=img,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        device=dev,
        max_det=max_det,
        verbose=False,
    )
    latency_ms = (time.perf_counter() - t0) * 1000.0

    r0 = results[0]
    out_boxes: List[Box] = []
    if r0.boxes is not None and len(r0.boxes) > 0:
        for b in r0.boxes:
            out_boxes.append(
                Box(
                    cls=int(b.cls.item()),
                    conf=float(b.conf.item()),
                    xyxy=[float(x) for x in b.xyxy[0].tolist()],
                )
            )

    names = getattr(r0, "names", None)
    return PredictResponse(
        model_key=model_key,
        local_model_path=LOCAL_MODEL_PATH,
        image_size=[w, h],
        boxes=out_boxes,
        names=names,
        latency_ms=float(latency_ms),
    )

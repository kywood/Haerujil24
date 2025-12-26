from fastapi import FastAPI
from Controller.IController import IController
from Config.ConfigLoader import ConfigLoader
from fastapi import UploadFile, File, Request, HTTPException

class ServingController(IController):

    def __init__(self,config: ConfigLoader):
        super().__init__()

        self._config = config

        from Dtos.S3Dto import S3ConnectDto
        self._s3ConnetctionDTO = S3ConnectDto().SetDTOFromConfig(config)

        # self.s3_endpoint = config.get("MINIO", "S3_ENDPOINT")
        # self.s3_bucket = config.get("MINIO", "S3_BUCKET")
        # self.s3_access_key = config.get("MINIO", "S3_ACCESS_KEY")
        # self.s3_secret_key = config.get("MINIO", "S3_SECRET_KEY")

        self.run_id = config.get("YOLO_MODEL", "RUN_ID")
        self.default_device = config.get("SERVING_RUNTIME", "YOLO_DEVICE", "auto")

        pass


    def register(self, app: FastAPI) -> None:
        """이 컨트롤러가 가진 엔드포인트들을 app에 등록"""

        @app.get("/health")
        def health():
            return {"status": "ok"}


        @app.get("/dir")
        def health_dir():
            from Config.ConfigHelper import ConfigHelper
            path = ConfigHelper.GetCachePath()

            print(f"path:{path}")

            return {"status": "ok"}


        from Models.RestModel import PingResponse
        # from Models.RestModel import PingRequest
        @app.get("/ping/{name}", response_model=PingResponse)
        def health_dir(name:str):
            # from Config.ConfigHelper import ConfigHelper
            # path = ConfigHelper.GetCachePath()
            # print(f"path:{path} nm:{name}")

            from Models.RestModel import ResponseHeader
            return PingResponse(response=ResponseHeader(code=1,message="dd"),  name="a" , age=10)


        # @app.post("/infer")
        # async def infer(request: Request,file: UploadFile = File(...)):
        #     ct = request.headers.get("content-type")
        #     print("content-type header:", ct)
        #
        #     print("=== Uploaded File Info ===")
        #     print("filename     :", file.filename)
        #     print("content_type :", file.content_type)
        #     content = await file.read()
        #     file_size = len(content)
        #     print("file_size    :", file_size, "bytes")
        #
        #     return {"status": "ok"}

        from Models.RestModel import InferResponse
        @app.post("/infer" , response_model=InferResponse)
        async def infer(request: Request,file: UploadFile = File(...)):
            import tempfile
            import os
            import time

            from Inference.InferenceManager import InferenceManager

            # 1) 업로드 파일을 임시 파일로 저장
            suffix = os.path.splitext(file.filename)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            try:
                # 2) 추론 실행
                mgr = InferenceManager.instance()

                t0 = time.time()
                results = mgr.infer(tmp_path)
                elapsed_ms = (time.time() - t0) * 1000.0

                # 3) 결과 파싱 (YOLO 결과 → JSON)
                r = results[0]
                detections = []
                boxes = r.boxes

                for i in range(len(boxes)):
                    cls_id = int(boxes.cls[i])
                    detections.append({
                        "class_id": cls_id,
                        "class_name": r.names.get(cls_id, str(cls_id)),
                        "confidence": float(boxes.conf[i]),
                        "bbox": list(map(float, boxes.xyxy[i])),  # [x1,y1,x2,y2]
                    })

                return InferResponse(
                    filename=file.filename,
                    elapsed_ms=elapsed_ms,
                    count=len(detections),
                    detections=detections
                )

                # return {
                #     "filename": file.filename,
                #     "elapsed_ms": elapsed_ms,
                #     "count": len(detections),
                #     "detections": detections
                # }

                # return JSONResponse({
                #     "filename": file.filename,
                #     "elapsed_ms": elapsed_ms,
                #     "count": len(detections),
                #     "detections": detections
                # })

            finally:
                # 임시파일 삭제
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass


        #
        #
        # @app.get("/download")
        # def health_download():
        #     from Config.ConfigHelper import ConfigHelper
        #     path = ConfigHelper.GetCachePath()
        #
        #     print(f"path:{path}")
        #
        #     from Inference.InferenceManager import InferenceManager
        #     InferenceManager.instance().DownloadModel()
        #
        #     return {"status": "ok"}



    pass

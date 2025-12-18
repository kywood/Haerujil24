import os
import argparse
import mlflow
from ultralytics import YOLO

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="dataset/data.yaml 경로")
    p.add_argument("--model", default="yolov8n.pt")
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--epochs", type=int, default=50)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--project", default="runs")
    p.add_argument("--name", default="train")
    p.add_argument("--mlflow_uri", default="http://localhost:5000")
    p.add_argument("--experiment", default="haerujil-yolo")
    p.add_argument("--device", default="0", help="CUDA device (e.g. 0, 0,1 or cpu)")
    args = p.parse_args()

    mlflow.set_tracking_uri(args.mlflow_uri)
    mlflow.set_experiment(args.experiment)

    # YOLO 학습
    yolo = YOLO(args.model)

    with mlflow.start_run(run_name=f"{os.path.basename(args.model)}_e{args.epochs}_b{args.batch}_s{args.imgsz}"):
        # 파라미터 기록
        mlflow.log_params({
            "model": args.model,
            "data": args.data,
            "imgsz": args.imgsz,
            "epochs": args.epochs,
            "batch": args.batch,
            "project": args.project,
            "name": args.name,
            "device": args.device,
        })

        results = yolo.train(
            data=args.data,
            imgsz=args.imgsz,
            epochs=args.epochs,
            batch=args.batch,
            project=args.project,
            name=args.name,
            device=args.device,
        )

        # Ultralytics가 저장한 run 폴더 찾기
        save_dir = getattr(results, "save_dir", None)
        if save_dir is None:
            # fallback (대부분 save_dir 존재)
            save_dir = os.path.join(args.project, args.name)

        save_dir = str(save_dir)

        # 대표 메트릭(가능하면 기록)
        # (Ultralytics 버전에 따라 키가 조금씩 다를 수 있음)
        try:
            metrics = results.results_dict if hasattr(results, "results_dict") else {}
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))
        except Exception:
            pass

        # 아티팩트 업로드: best.pt / last.pt / plots 등
        # weights
        weights_dir = os.path.join(save_dir, "weights")
        for fn in ["best.pt", "last.pt"]:
            fp = os.path.join(weights_dir, fn)
            if os.path.exists(fp):
                mlflow.log_artifact(fp, artifact_path="weights")

        # plots/results
        for fn in ["results.png", "confusion_matrix.png", "confusion_matrix_normalized.png"]:
            fp = os.path.join(save_dir, fn)
            if os.path.exists(fp):
                mlflow.log_artifact(fp, artifact_path="plots")

        # args.yaml도 같이 올리면 재현성 좋아짐
        args_yaml = os.path.join(save_dir, "args.yaml")
        if os.path.exists(args_yaml):
            mlflow.log_artifact(args_yaml, artifact_path="meta")

        print(f"[OK] Logged to MLflow. save_dir={save_dir}")

if __name__ == "__main__":
    main()
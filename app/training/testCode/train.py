import os
os.environ["MLFLOW_DISABLED"] = "true"

import argparse
import mlflow
from ultralytics import YOLO
import boto3

def s3_upload(local_path: str, bucket: str, key: str, endpoint_url: str, access_key: str, secret_key: str, region: str = "us-east-1"):
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    s3.upload_file(local_path, bucket, key)

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

    p.add_argument("--s3_endpoint", default="http://127.0.0.1:9000")
    p.add_argument("--s3_bucket", default="mlflow")
    p.add_argument("--s3_prefix", default="yolo-artifacts")  # 버킷 아래 폴더
    p.add_argument("--s3_access_key", default="oracle")
    p.add_argument("--s3_secret_key", default="oracleoracle")
    p.add_argument("--s3_region", default="us-east-1")

    args = p.parse_args()

    os.environ["MLFLOW_DISABLED"] = "true"

    mlflow.set_tracking_uri(args.mlflow_uri)
    mlflow.set_experiment(args.experiment)

    # YOLO 학습
    yolo = YOLO(args.model)

    with mlflow.start_run(run_name=f"{os.path.basename(args.model)}_e{args.epochs}_b{args.batch}_s{args.imgsz}") as run:
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

        run_id = run.info.run_id
        # run_id = mlflow.active_run().info.run_id

        save_dir = str(getattr(results, "save_dir", os.path.join(args.project, args.name)))

        # metrics 기록(가능하면)
        try:
            metrics = results.results_dict if hasattr(results, "results_dict") else {}
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))
        except Exception:
            pass

        # ✅ weights/plots는 MinIO(S3)로 직접 업로드

        base_prefix = f"{args.s3_prefix}/{args.experiment}/{run_id}"

        # weights
        weights_dir = os.path.join(save_dir, "weights")
        for fn in ["best.pt", "last.pt"]:
            fp = os.path.join(weights_dir, fn)
            if os.path.exists(fp):
                key = f"{base_prefix}/weights/{fn}"
                s3_upload(fp, args.s3_bucket, key, args.s3_endpoint, args.s3_access_key, args.s3_secret_key, args.s3_region)

        # plots
        for fn in ["results.png", "confusion_matrix.png", "confusion_matrix_normalized.png", "args.yaml"]:
            fp = os.path.join(save_dir, fn)
            if os.path.exists(fp):
                key = f"{base_prefix}/misc/{fn}"
                s3_upload(fp, args.s3_bucket, key, args.s3_endpoint, args.s3_access_key, args.s3_secret_key, args.s3_region)

        print(f"[OK] MLflow run={run_id}, save_dir={save_dir}")
        print(f"[OK] Uploaded to s3://{args.s3_bucket}/{base_prefix}/ ...")

if __name__ == "__main__":
    main()
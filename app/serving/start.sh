#!/usr/bin/env bash
set -e

# 학습 스크립트와 동일하게 맞추면 됨
export S3_ENDPOINT=${S3_ENDPOINT:-http://127.0.0.1:9000}
export S3_BUCKET=${S3_BUCKET:-mlflow}
export S3_PREFIX=${S3_PREFIX:-yolo-artifacts}
export EXPERIMENT=${EXPERIMENT:-haerujil-yolo}

# 여기만 네 run_id로 지정!
export RUN_ID=${RUN_ID:-YOUR_RUN_ID_HERE}

export S3_ACCESS_KEY=${S3_ACCESS_KEY:-oracle}
export S3_SECRET_KEY=${S3_SECRET_KEY:-oracleoracle}
export S3_REGION=${S3_REGION:-us-east-1}

# GPU면 "0", CPU면 "cpu", 자동이면 "auto"
export YOLO_DEVICE=${YOLO_DEVICE:-auto}

uvicorn app.main:app --host 0.0.0.0 --port 8000
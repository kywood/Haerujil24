from Defs.IEnum import IENUM


class ConfigDefine:

    class E_SECTION(IENUM):
        MINIO="MINIO"

        YOLO_MODEL = "YOLO_MODEL"
        SERVING_RUNTIME="SERVING_RUNTIME"
        SECURITY="SECURITY"
        SERVER="SERVER"



    class E_MINIO(IENUM):
        S3_ENDPOINT="S3_ENDPOINT"
        S3_BUCKET="S3_BUCKET"
        S3_ACCESS_KEY="S3_ACCESS_KEY"
        S3_SECRET_KEY="S3_SECRET_KEY"
        S3_REGION="S3_REGION"

        pass

    class E_YOLO_MODEL(IENUM):
        S3_PREFIX="S3_PREFIX"
        EXPERIMENT="EXPERIMENT"
        RUN_ID="RUN_ID"
        pass

    class E_SERVING_RUNTIME(IENUM):
        YOLO_DEVICE="YOLO_DEVICE"
        INFER_CONCURRENCY="INFER_CONCURRENCY"
        MAX_IMAGE_PIXELS="MAX_IMAGE_PIXELS"
        pass

    class E_SECURITY(IENUM):
        RELOAD_TOKEN="RELOAD_TOKEN"

        pass

    class E_SERVER(IENUM):
        HOST="HOST"
        PORT="PORT"
        WORKERS="WORKERS"
        pass

    pass
FROM python:3.11-slim

# ffmpeg + ffprobe 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY build_dataset.py /app/build_dataset.py

# 컨테이너 실행 시 python 스크립트가 바로 실행되게
ENTRYPOINT ["python", "/app/build_dataset.py"]

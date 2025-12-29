FROM python:3.11-slim

WORKDIR /work

# 빌드/업로드 도구 설치
RUN pip install --no-cache-dir -U build twine tomlkit

# common_lib 소스 복사
COPY . /work

# 실행 시: 버전 주입 -> build -> upload
ENTRYPOINT ["python", "tools/set_version_and_upload.py"]

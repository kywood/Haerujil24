from pathlib import Path
from typing import Iterable, Sequence

from botocore.exceptions import ClientError

from common_lib.ObjectStorage.ObjectStat import ObjectStat
from common_lib.ObjectStorage.ObjectStorage import ObjectStorage
from common_lib.ObjectStorage.ObjectStorageConnection import ObjectStorageConnection, MinioConnection


class MinioObjectStorage(ObjectStorage):

    def __init__(self , s3_client , bucket):
        super().__init__()
        self._s3 = s3_client
        self._bucket = bucket
        pass

    # listing
    def ls(self, prefix: str = "") -> Iterable[str]:
        """
              1-depth ls 느낌:
              - delimiter='/' 로 현재 depth의 파일 + 하위 prefix(폴더처럼 보이는 것) 반환
              - 폴더 prefix는 trailing '/' 포함
              """
        resp = self._s3.list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
            Delimiter="/",
        )

        # 하위 폴더처럼 보이는 prefix
        for p in resp.get("CommonPrefixes", []):
            yield p["Prefix"]

        # 현재 depth의 파일
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            # prefix 그 자체(폴더 placeholder)만 있는 경우 제외하고 싶으면 유지
            if key != prefix:
                yield key

    def walk(self, prefix: str = "") -> Iterable[str]:
        """prefix 하위 전체(재귀)"""
        paginator = self._s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                yield obj["Key"]

    # write
    def puts(self, items: Sequence[tuple[str, str]]) -> None:
        """[(local_path, key), ...]"""
        for local_path, key in items:
            lp = Path(str(local_path))
            if not lp.is_file():
                raise FileNotFoundError(f"Local file not found: {lp}")
            self._s3.upload_file(str(lp), self._bucket, key)

    # read
    def get(self, key: str, local_path: str) -> None:
        lp = Path(local_path)
        lp.parent.mkdir(parents=True, exist_ok=True)
        self._s3.download_file(self._bucket, key, str(lp))

    # meta
    def stat(self, key: str) -> ObjectStat | None:
        try:
            resp = self._s3.head_object(Bucket=self._bucket, Key=key)

            etag = resp.get("ETag")
            if isinstance(etag, str):
                etag = etag.strip('"')

            return ObjectStat(
                key=key,
                size=int(resp.get("ContentLength", 0)),
                last_modified=resp.get("LastModified"),
                etag=etag,
            )

        except ClientError as e:
            code = e.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey", "NotFound"):
                return None
            raise

    def exists(self, key: str) -> bool:
        try:
            self._s3.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey", "NotFound"):
                return False
            raise

    # delete
    def delete(self, key: str) -> None:
        # S3/MinIO는 존재하지 않아도 보통 성공 처리됨
        self._s3.delete_object(Bucket=self._bucket, Key=key)

    def mkdir(self, key: str) -> None:
        """
                S3/MinIO에는 폴더가 없으므로 'prefix/' 0바이트 객체를 만들어 폴더처럼 보이게 함.
                """
        prefix = key if key.endswith("/") else key + "/"
        self._s3.put_object(Bucket=self._bucket, Key=prefix, Body=b"")

    pass
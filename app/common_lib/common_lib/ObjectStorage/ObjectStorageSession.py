from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from common_lib.ObjectStorage.ObjectStorageConnection import MinioConnection


class ObjectStorageSession(ABC):

    @abstractmethod
    def __enter__(self) -> "ObjectStorageSession":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc, tb) -> bool:
        raise NotImplementedError

    @abstractmethod
    def storage(self, bucket_or_container: str):
        """세션에서 특정 버킷/컨테이너를 대상으로 하는 ObjectStorage를 만든다."""
        raise NotImplementedError

    @property
    @abstractmethod
    def client(self):
        raise NotImplementedError

    pass


class MinioSession(ObjectStorageSession):

    def __init__(self , objectStorageConnection ):

        self._objectStorageConnection = objectStorageConnection
        from typing import Optional
        self._s3: Optional[object] = None
        pass


    def __enter__(self) -> "MinioSession":
        c = self._objectStorageConnection

        self._s3 = boto3.client(
            "s3",
            endpoint_url=c.endpoint,
            aws_access_key_id=c.access_key,
            aws_secret_access_key=c.secret_access_key,
            region_name=c.region_name,
##            verify=c.verify_ssl,
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._s3 is not None:
            # botocore client는 close() 지원
            try:
                self._s3.close()
            finally:
                self._s3 = None
        # False -> 예외 발생 시 그대로 전파
        return False

    @property
    def client(self):
        if self._s3 is None:
            raise RuntimeError("Session not connected")
        return self._s3

    def storage(self, bucket_or_container: str):
        """세션에서 특정 버킷을 대상으로 하는 MinioObjectStorage를 만든다."""
        if self._s3 is None:
            raise RuntimeError("MinioSession is not connected. Use `with MinioSession(...) as s:`")

        from common_lib.ObjectStorage.MinioObjectStorage import MinioObjectStorage

        return MinioObjectStorage(s3_client=self._s3, bucket=bucket_or_container)
    pass
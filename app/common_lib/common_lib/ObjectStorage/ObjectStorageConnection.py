from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import ContextManager

from common_lib.Dtos.IDto import IDTO
from common_lib.ObjectStorage.ObjectStorage import ObjectStorage
from common_lib.ObjectStorage.ObjectStorageSession import ObjectStorageSession, MinioSession


class ObjectStorageConnection(IDTO):

    def __init__(self,
                 endpoint,
                 user_name,
                 password,
                 region_name,
                 bucket_name = None
                 ):
        super().__init__()

        self.endpoint = endpoint
        self.access_key = user_name
        self.secret_access_key = password
        self.region_name = region_name
        self.bucket_name = bucket_name
        pass


    @abstractmethod
    def GetSession(self) -> ContextManager[ObjectStorageSession]:
        """with connection.con() as session: ..."""
        raise NotImplementedError


    @abstractmethod
    def GetStorage(self) -> ContextManager[ObjectStorage]:
        """with connection.con() as session: ..."""
        raise NotImplementedError


class MinioConnection(ObjectStorageConnection):

    def GetSession(self) -> ContextManager[ObjectStorageSession]:
        # 여기서는 세션 객체만 만들고
        # 실제 boto3.client 생성은 MinioSession.__enter__에서 발생
        return MinioSession(self)


    # def GetStorage(self) -> ContextManager[ObjectStorage]:
    #     session= MinioSession(self)
    #     return session.storage( self.bucket_name )
    #     # MinioObjectStorage( session. )


    @contextmanager
    def GetStorage(self):
        if not self.bucket_name:
            raise ValueError("bucket_name is required")

        with MinioSession(self) as session:
            storage = session.storage(self.bucket_name)  # ✅ 여기선 연결되어 있음
            yield storage
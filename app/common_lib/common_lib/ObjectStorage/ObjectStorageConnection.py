from abc import ABC, abstractmethod
from typing import ContextManager

from common_lib.Dtos.IDto import IDTO
from common_lib.ObjectStorage.ObjectStorageSession import ObjectStorageSession, MinioSession


class ObjectStorageConnection(IDTO):

    def __init__(self):

        pass


    @abstractmethod
    def con(self) -> ContextManager[ObjectStorageSession]:
        """with connection.con() as session: ..."""
        raise NotImplementedError


class MinioConnection(ObjectStorageConnection):


    def __init__(self ,
                 endpoint ,
                 user_name ,
                 password ,
                 region_name
                 ):

        super().__init__()

        self.endpoint = endpoint
        self.access_key = user_name
        self.secret_access_key = password
        self.region_name = region_name

        pass

    def con(self) -> ContextManager[ObjectStorageSession]:
        # 여기서는 세션 객체만 만들고
        # 실제 boto3.client 생성은 MinioSession.__enter__에서 발생
        return MinioSession(self)

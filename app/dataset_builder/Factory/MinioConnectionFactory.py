from common_lib.Config.ConfigLoader import ConfigLoader
from common_lib.Path.BasePath import BasePath

from Factory.Factory import IFactory


class MinioConnectionFactory(IFactory):

    @staticmethod
    def GetConnection(  configLoader:ConfigLoader ):
        from common_lib.ObjectStorage.ObjectStorageConnection import MinioConnection
        # print("i'm factory")
        # pp= configLoader.Get(section="MINIO",key="S3_ENDPOINT")
        from Defines.ConfigDefine import ConfigDefine

        minioConnection = MinioConnection(
            endpoint = configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_ENDPOINT) ,
            region_name=configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_REGION) ,
            user_name=configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_ACCESS_KEY) ,
            password=configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_SECRET_KEY) ,
            bucket_name=configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_BUCKET)

        )

        return minioConnection





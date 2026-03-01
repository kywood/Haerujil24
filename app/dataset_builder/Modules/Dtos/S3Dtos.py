from common_lib.Config.ConfigLoader import ConfigLoader
from common_lib.Dtos.S3Dto import S3ConnectDto


class S3ConnectDtoEx(S3ConnectDto):

    def __init__(self):
        super().__init__()

    def SetDTOFromConfig(self , config:ConfigLoader ):
        from Defines.ConfigDefine import ConfigDefine

        self.s3_endpoint = config.Get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_ENDPOINT )
        self.bucket = config.Get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_BUCKET )
        self.access_key = config.Get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_ACCESS_KEY )
        self.secret_access_key = config.Get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_SECRET_KEY )
        self.region_name = config.Get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_REGION )
        return self


    pass



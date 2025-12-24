from Config.ConfigLoader import ConfigLoader
from Dtos.IDto import IDTO


class S3Dto(IDTO):

    def __init__(self):
        super().__init__()

    pass

class S3ConnectDto(IDTO):

    def __init__(self):
        super().__init__()
        self.s3_endpoint = None
        self.bucket = None
        self.access_key = None
        self.secret_access_key = None
        self.region_name = None
        pass

    def SetDTO(self , s3_endpoint , bucket , access_key ,  secret_access_key , region_name ):
        self.s3_endpoint = s3_endpoint
        self.bucket = bucket
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        return self

    def SetDTOFromConfig(self , config:ConfigLoader ):
        from Config.ConfigDefines import ConfigDefine
        self.s3_endpoint = config.get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_ENDPOINT )
        self.bucket = config.get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_BUCKET )
        self.access_key = config.get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_ACCESS_KEY )
        self.secret_access_key = config.get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_SECRET_KEY )
        self.region_name = config.get(ConfigDefine.E_SECTION.MINIO ,ConfigDefine.E_MINIO.S3_REGION )
        return self


    def __repr__(self) -> str:
        # 민감정보 노출 방지(시크릿은 마스킹)
        return (
            "S3ConnectDto("
            f"s3_endpoint={self.s3_endpoint!r}, "
            f"access_key={'<ACCESS_KEY>' if self.access_key else ''}, "
            f"bucket={'<BUCKET>' if self.bucket else ''}, "
            f"secret_access_key={'<SECRET>' if self.secret_access_key else ''}, "
            f"region_name={self.region_name!r})"
        )

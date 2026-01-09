




class ConfigHelper:

    #
    # @staticmethod
    # def GetMinioEndpoint(configLoader):
    #     from Defines.ConfigDefine import ConfigDefine
    #     return configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
    #                      key=ConfigDefine.E_MINIO.S3_ENDPOINT)

    @staticmethod
    def GetMinioEndpoint(configLoader):
        from Defines.ConfigDefine import ConfigDefine
        return configLoader.Get(section=ConfigDefine.E_SECTION.MINIO,
                         key=ConfigDefine.E_MINIO.S3_ENDPOINT)


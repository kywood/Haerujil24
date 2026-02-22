from common_lib.Config.ConfigLoader import ConfigLoader


class ExtractorUtils:

    @staticmethod
    def GetTmpDirName(configLoader: ConfigLoader, processName):
        from Defines.ConfigDefine import ConfigDefine

        tmpDirBase = configLoader.Get(
            section=ConfigDefine.E_SECTION.EXTRACT,
            key=ConfigDefine.E_EXTRACT.TMP_DIR_NAME
        )

        from pathlib import Path
        return str(Path(".") / tmpDirBase / processName)


    @staticmethod
    def GetExtractorPrefix(configLoader: ConfigLoader):
        from Defines.ConfigDefine import ConfigDefine

        extractorPrefix = configLoader.Get(
            section=ConfigDefine.E_SECTION.EXTRACT,
            key=ConfigDefine.E_EXTRACT.EXT_DIR_NAME
        )

        return extractorPrefix


    @staticmethod
    def GetS3UnNormalDirName(configLoader: ConfigLoader):
        from Defines.ConfigDefine import ConfigDefine

        extractorPrefix = configLoader.Get(
            section=ConfigDefine.E_SECTION.EXTRACT,
            key=ConfigDefine.E_EXTRACT.S3_UNNORMAL_DIR_NAME
        )

        return extractorPrefix


    @staticmethod
    def GetS3NormalDirName(configLoader: ConfigLoader):
        from Defines.ConfigDefine import ConfigDefine

        extractorPrefix = configLoader.Get(
            section=ConfigDefine.E_SECTION.EXTRACT,
            key=ConfigDefine.E_EXTRACT.S3_NORMAL_DIR_NAME
        )

        return extractorPrefix


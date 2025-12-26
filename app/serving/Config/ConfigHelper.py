


class ConfigHelper:


    # @staticmethod
    # def GetCachePath():
    #     from Config.ConfigLoader import ConfigLoader
    #     from Config.ConfigDefines import ConfigDefine
    #     return ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
    #                                 ConfigDefine.E_INFERENCE_MODEL.CACHE_PATH)

    @staticmethod
    def GetConfig():
        from Config.ConfigLoader import ConfigLoader
        return ConfigLoader.instance()

    @staticmethod
    def GetModelUrl():
        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        return ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.MODEL_URL)

    @staticmethod
    def GetModelRemotePath():
        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        modelUrl = ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.MODEL_URL)
        modelName = ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                               ConfigDefine.E_INFERENCE_MODEL.MODEL_NAME)

        return modelUrl + "/" + modelName



    @staticmethod
    def GetModelName():
        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        return ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.MODEL_NAME)

    @staticmethod
    def GetBasePath():
        from pathlib import Path
        return Path(__file__).resolve().parents[1]


    @staticmethod
    def GetCachePath():

        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        cache_dir_name = ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.CACHE_PATH)

        return ConfigHelper.GetBasePath() / cache_dir_name

    @staticmethod
    def GetLocalCachePath():
        return ConfigHelper.GetCachePath() / ConfigHelper.GetModelName()


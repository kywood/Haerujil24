


class ConfigHelper:


    @staticmethod
    def GetCachePath():
        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        return ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.CACHE_PATH)

    @staticmethod
    def GetModelUrl():
        from Config.ConfigLoader import ConfigLoader
        from Config.ConfigDefines import ConfigDefine
        return ConfigLoader.instance().get(ConfigDefine.E_SECTION.INFERENCE_MODEL,
                                    ConfigDefine.E_INFERENCE_MODEL.MODEL_URL)
from Utils.Singleton import SingletonBase


class InferenceModelManager(SingletonBase):

    def __init__(self , config):
        SingletonBase.__init__(self)
        self._config = config

        from pathlib import Path
        from Config.ConfigHelper import ConfigHelper


        self.cache_dir = Path(ConfigHelper.GetCachePath())
        self.model_url = config.get("MODEL_URL")  # 다운로드 주소
        self.model_name = config.get("MODEL_NAME", "model.bin")


        pass

    



    def Println(self):

        pass


    pass

# #
# config=10
# #
# InferenceModelManager.instance(config=config)
#
# InferenceModelManager.instance().Println()
# # # InferenceModelManager(config=config)
# #

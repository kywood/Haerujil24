from abc import ABC


class ConfiguableProcess(ABC):

    def __init__(self):
        self._configLoader  =None
        pass

    def ConfigLoader(self):
        from common_lib.Path.BasePath import BasePath
        from Defines.Defines import Defines
        from common_lib.Config.ConfigLoader import ConfigLoader

        config_file = BasePath.instance().File(Defines.CONFIG_FILE_NAME)
        self._configLoader = ConfigLoader.instance(config_file)

        pass

    pass
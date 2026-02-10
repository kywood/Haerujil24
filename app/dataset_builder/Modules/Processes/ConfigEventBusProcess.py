from common_lib.multiProcess.abProcess import eventBusProcess

from Modules.Processes.ConfiguableProcess import ConfiguableProcess


class ConfigEventBusProcess(eventBusProcess, ConfiguableProcess):

    def PostInit(self):
        super().PostInit()
        self.ConfigLoader()


    pass
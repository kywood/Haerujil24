from typing import List
from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
from common_lib.MessageQueue.MessageHandler import MessageHandler

from Modules.Processes.ConfigEventBusProcess import ConfigEventBusProcess


class WorkerProcess(ConfigEventBusProcess):

    def __init__(self,
                 ipcController: IPC_Controller,
                 channelDtos: List[ChannelDTO],
                 messageHandler: MessageHandler,
                 name: str = "None",
                 ):
        super().__init__(
            name=name,
            ipcController=ipcController ,
            channelDtos=channelDtos ,
            messageHandler=messageHandler)

    def CallProcessing(self, process):

        pass


    pass


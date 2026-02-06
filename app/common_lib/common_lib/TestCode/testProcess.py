import time
from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
from common_lib.MessageQueue.MessageHandler import MessageHandler
from common_lib.MessageQueue.MessageQueue import IMessageQueue
from common_lib.multiProcess.abProcess import eventBusProcess


class cProducerProcess(eventBusProcess):

    def __init__(self,
                 ipcController: IPC_Controller,
                 channelDtos: List[ChannelDTO],
                 messageHandler: MessageHandler,
                 name: str = "None",
                 ):
        super().__init__(name=name,
            ipcController=ipcController ,
            channelDtos=channelDtos ,
            messageHandler=messageHandler)

        self._loop=0
        pass

    def CallProcessing(self, process):
        # print("cProducerProcess :: CallProcessing Send >> ")


        self.GetEventBus().Send("COMQ", f" [cProducerProcess] [{self.GetName()}] cProducerMessage  {self._loop} ")
        # self.GetEventBus().Send("PQ", f" PQ >>>>>>>>>>>>>>>> {self._loop} ")
        self._loop=self._loop+1

        time.sleep(1)
        ## packet produsing
        pass
    pass

class cConsumerProcess(eventBusProcess):

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

        self._loop = 0

        pass

    #
    def CallProcessing(self, process):

        # print("cConsumerProcess :: CallProcessing~")

        self.GetEventBus().Send("COMQ" ,f" [cConsumerProcess] [{self.GetName()}]   cConsumerMessage  {self._loop} " )

        ## packet consumeing
        self._loop = self._loop + 1

        time.sleep(1)

        pass

    pass


import time
from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.MessageHandler import MessageHandler
from common_lib.MessageQueue.MessageQueue import IMessageQueue
from common_lib.multiProcess.abProcess import eventBusProcess


class cProducerProcess(eventBusProcess):

    def __init__(self,
                 messageQueue: IMessageQueue,
                 channelDtos: List[ChannelDTO],
                 messageHandler: MessageHandler,
                 name: str = "None",
                 ):
        super().__init__(name=name,
            messageQueue=messageQueue ,
            channelDtos=channelDtos ,
            messageHandler=messageHandler)

        self._loop=0

        pass

    def CallProcessing(self, process):
        # print("cProducerProcess :: CallProcessing Send >> ")
        self.GetEventBus().Send("COMQ", f" COMQ >>>>>>>>>>>>>>>> {self._loop} ")

        self.GetEventBus().Send("PQ", f" PQ >>>>>>>>>>>>>>>> {self._loop} ")

        self._loop=self._loop+1


        time.sleep(1)
        ## packet produsing
        pass
    pass

class cConsumerProcess(eventBusProcess):

    def __init__(self,
                 messageQueue: IMessageQueue,
                 channelDtos: List[ChannelDTO],
                 messageHandler: MessageHandler,
                 name: str = "None",
                 ):
        super().__init__(
            name=name,
            messageQueue=messageQueue ,
            channelDtos=channelDtos ,
            messageHandler=messageHandler)
        pass

    #
    def CallProcessing(self, process):

        # print("cConsumerProcess :: CallProcessing~")

        # self.GetEventBus().Send("COMQ" ,"protocol" )

        ## packet consumeing


        pass

    pass


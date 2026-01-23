import time
from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.MessageHandler import MessageHandler
from common_lib.MessageQueue.MessageQueue import IMessageQueue


class IProcess:
    def GetName(self):
        pass

    def GetRunning(self):
        pass
    def CallProcessing(self, process):
        pass
    def HandleProcess(self, process):
        pass

class abProcess(IProcess):

    # seqGenerator = cSequenceNumberMultiProcessor()
    def __init__(self, name):
        # self.name = _name
        self._name = name

        # self._isRunning = False
        # self._sharedQueue = None
        # self._lock = None
    #
    def GetName(self):
        return self._name
    #
    # def _setStart(self):
    #     self._isRunning = True
    #
    # def _setStop(self):
    #     self._isRunning = False
    #
    # def GetRunning(self):
    #     return self._isRunning
    #
    # def Running(self, process):
    #     for i in range(2)
    #         print("abProcess " + self._name + " " + str(i))
    #         import time
    #         time.sleep(1)
    #
    # def Action(self, process):
    #     try:
    #         self._setStart()
    #         self.Running(process)
    #         self._setStop()
    #     except Exception as e:
    #         self._setStop()
    #         raise e

class EventProcess(abProcess):

    def __init__(self,
                 name):
        super().__init__(name)
        self._eventBus = None
        self._tryException = None

        pass

    def _setStart(self):
        self.PostInit()
        self.Start()
        self._isRunning = True

    def _setStop(self):
        self._isRunning = False
        self.Stop()

    def GetRunning(self):
        return self._isRunning

    def CallProcessing(self, process):

        print("abProcess " + self._name)
        #
        # import time
        #
        # while True:
        #     print("abProcess " + self._name )
        #     time.sleep(1)
        #     pass

        # for i in range(2):
        #     print("abProcess " + self._name + " " + str(i))
        #     import time
        #     time.sleep(1)

    def HandleProcess(self, process):
        try:
            self._setStart()

            while self._isRunning:

                self.CallProcessing(process)
                # time.sleep(0.02)
                time.sleep(0.0)

            self._setStop()
        except Exception as e:
            self._setStop()
            raise e

    def PostInit(self):

        pass

    def SetEventBus(self, event_bus):
        self._eventBus = event_bus

    def GetEventBus(self):
        return self._eventBus


    def Start(self):

        self.PostInit()

        if self._eventBus != None:
            self._eventBus.Start()

    def Stop(self):
        if self._eventBus != None:
            self._eventBus.Stop()

    def TryException(self, e):
        self._tryException = e

    def IsTryException(self):
        if self._tryException is None:
            return False
        return True

    def GetTryException(self):
        return self._tryException

    def ClearException(self):
        self._tryException = None

class cTestProcess(EventProcess):

    def __init__(self):
        super().__init__(self)
        pass

    pass

class eventBusProcess(EventProcess):
### TODO 100
## parent mp

    def __init__(self ,
                 name:str,
                 messageQueue : IMessageQueue ,
                 channelDtos :List[ChannelDTO],
                 messageHandler : MessageHandler ):
        super().__init__(name=name)

        self._messageQueue = messageQueue
        # self._channelLists = channelLists
        self._messageHandler = messageHandler

        self._channelDtos = channelDtos


    def PostInit(self):
        from common_lib.MessageQueue.EventBus import EventBus
        self.SetEventBus(EventBus(self, self._messageQueue ))

        channels = []
        for channelDto in self._channelDtos:
            channels.append(
                self._eventBus.CreateMessageChannel(
                    channelDto.channel_name , channelDto.channel_type
                )
            )

        from common_lib.MessageQueue.EventListener import EventListener
        self._eventBus.AddListener(
            EventListener().AppendChannels(channels).SetMessageHandler(self._messageHandler)
        )
        pass


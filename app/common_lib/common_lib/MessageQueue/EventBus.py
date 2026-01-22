from abc import abstractmethod

from common_lib.MessageQueue.MessageQueue import IMessageQueue
from common_lib.multiProcess.abProcess import EventProcess


class IBus:

    def __init__(self):
        pass

    @abstractmethod
    def GetMessageQueue(self):
        pass

    @abstractmethod
    def GetParentProcess(self):
        pass

    pass

class EventBus(IBus):

    def __init__(self,
                 parent_process: EventProcess = None,
                 message_queue: IMessageQueue = None
                 ):
        super().__init__()

        self._parent_process = parent_process

        self._messageQueue = message_queue
        from common_lib.MessageQueue.MessageChannelContainer import MessageChannelContainer
        self._messageChannelContainer = MessageChannelContainer(message_queue)

        #################################################################################

        from common_lib.MessageQueue.EventListenerContainer import EventListenerContainer
        self._eventListenerContainer = EventListenerContainer(self)

        pass

    def GetEventListenerContainer(self):
        return self._eventListenerContainer

    def CreateMessageChannel(self,
                             channel_name,
                             channel_type
                             ):
        # from ody_lib.message_queue.cMessageChannel import cMessageChannel

        if self._messageChannelContainer.IsContainChannel(channel_name, channel_type) == False:
            from common_lib.MessageQueue.MessageChannel import MessageChannel
            messageChannel = MessageChannel(channel_name, channel_type).Build(self._messageChannelContainer)
            # self._messageChannelContainer.AppendChannel(cMessageChannel(channel_name, channel_type).Build(self._messageChannelContainer))
            self._messageChannelContainer.AppendChannel(messageChannel)

            return messageChannel

        return None

    def AddListener(self, event_listener):
        event_listener.SetEventBus(self)
        self.GetEventListenerContainer().AddListener(event_listener)

    def AppendChannel(self, message_channel):
        self.GetMessageChannelContainer().AppendChannel(message_channel)

    def GetChannel(self, channel_name):
        return self.GetMessageChannelContainer().GetChannel(channel_name)

    def GetMessageChannelContainer(self):
        return self._messageChannelContainer

    def Start(self):

        self._eventListenerContainer.Start()
        pass

    def Stop(self):
        self._eventListenerContainer.Stop()
        pass

    def IsStoped(self):
        return self._eventListenerContainer.IsStoped()

    def Send(self, channel_nm, protocol):
        self._messageChannelContainer.Push(channel_nm, protocol)
        pass

    @abstractmethod
    def GetMessageQueue(self):
        return self._messageQueue

    @abstractmethod
    def GetParentProcess(self):
        return self._parent_process

    pass

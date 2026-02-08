from abc import abstractmethod

from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
# from common_lib.MessageQueue.MessageChannelController import MessageChannelController
from common_lib.multiProcess.abProcess import EventProcess


class IBus:

    def __init__(self):
        pass

    # @abstractmethod
    # def GetMessageQueue(self):
    #     pass

    @abstractmethod
    def GetParentProcess(self):
        pass

    @abstractmethod
    def GetMessageChannel(self , channel_name ):


        pass

    pass

class EventBus(IBus):

    def __init__(self,
                 parent_process: EventProcess = None,
                 ipcController: IPC_Controller = None
                 ):
        super().__init__()

        self._parent_process = parent_process

        self._ipcController = ipcController

        # self._messageQueue = message_queue
        from common_lib.MessageQueue.MessageChannelController import MessageChannelController
        self._messageChannelContainer = MessageChannelController( self )

        #################################################################################

        from common_lib.MessageQueue.EventListenerContainer import EventListenerContainer
        self._eventListenerContainer = EventListenerContainer(self)

        pass

    def GetEventListenerContainer(self):
        return self._eventListenerContainer
    #
    def CreateMessageChannel(self,
                             channel_name,
                             channel_type
                             ):

        if self._messageChannelContainer.IsContainChannel(channel_name, channel_type) == False:

            from common_lib.MessageQueue.MessageChannel import MessageChannelFactory

            channelIPC = self._ipcController.GetChannelIPC(channel_name)
            messageChannel = MessageChannelFactory.CreateMessageChennel(channelIPC, channel_type)

            self._messageChannelContainer.AppendMessageChannel(messageChannel)

            return messageChannel

        return None

    def AddListener(self, event_listener):
        event_listener.SetEventBus(self)
        self.GetEventListenerContainer().AddListener(event_listener)
    #
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

    def Send(self, channel_name, protocol):

        messageChannel = self._messageChannelContainer.GetMessageChannel(
            channel_name=channel_name
        )

        messageChannel.Push(protocol)
        pass

    @abstractmethod
    def GetMessageChannel(self, channel_name):
        return self._messageChannelContainer.GetMessageChannel(
            channel_name=channel_name
        )

    @abstractmethod
    def GetParentProcess(self):
        return self._parent_process

    pass

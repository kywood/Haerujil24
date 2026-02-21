from abc import ABC, abstractmethod

from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE
from common_lib.MessageQueue.IPCS.IPCController import ChannelIPC
from common_lib.MessageQueue.IPCS.IPCInterface import IQueueType, IHSetType
from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR


class IMessageChannel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def GetChannelName(self):
        pass

    @abstractmethod
    def GetChannelType(self):
        pass

    ##: MessageChannelController
    @abstractmethod
    def SetMessageChannelController(self , messageChannelController ):
        pass

    @abstractmethod
    def GetIPC(self):

        pass

    pass


class abMessageChannel(IMessageChannel , ABC):

    def __init__(self , ipc ,
                 channel_name ,
                 channel_type : E_CHANNEL_TYPE):
        super().__init__()
        self._ipc = ipc

        self._channelName = channel_name
        self._channelType = channel_type

        self._messageChannelController = None
        pass

    def GetChannelName(self):
        return self._channelName

    def GetChannelType(self):
        return self._channelType


    ##: MessageChannelController
    def SetMessageChannelController(self , messageChannelController ):
        self._messageChannelController = messageChannelController
        pass

    def GetIPC(self):
        return self._ipc


class MessageChannelQueue(abMessageChannel,IQueueType):

    def __init__(self,ipc, channel_name , channel_type : E_CHANNEL_TYPE):
        super().__init__(ipc, channel_name , channel_type)
        pass

    def _GetPipeType(self , protocol_dir : E_PROTOCOL_DIR):

        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE

        if self.GetChannelType() is E_CHANNEL_TYPE.SERVER:

            if protocol_dir == E_PROTOCOL_DIR.SEND:
                return E_PIPE_TYPE.SERVER_TO_CLIENT
            return E_PIPE_TYPE.CLIENT_TO_SERVER
        else:

            if protocol_dir == E_PROTOCOL_DIR.SEND:
                return E_PIPE_TYPE.CLIENT_TO_SERVER
            return E_PIPE_TYPE.SERVER_TO_CLIENT


    def Push(self , protocol ):
        pipe_type = self._GetPipeType(E_PROTOCOL_DIR.SEND)
        self._ipc.Push( pipe_type = pipe_type , protocol=protocol )

    def Pop(self):
        pipe_type = self._GetPipeType(E_PROTOCOL_DIR.RECV)
        return self._ipc.Pop( pipe_type)


class MessageChannelHSet(abMessageChannel,IHSetType):

    def __init__(self,ipc, channel_name, channel_type:E_CHANNEL_TYPE):
        super().__init__(ipc, channel_name, channel_type)

        pass

    def Set(self , key , value ):
        self._ipc.Set(key , value)

    def Get(self , key ):

        return self._ipc.Get(key)

    def Clear(self):

        self._ipc.Clear()

    def IsContain(self ,key):
        return self._ipc.IsContain(key)

    def pp(self):
        print("aaaaaaaaaaaaaaa")



class MessageChannelFactory:

    @staticmethod
    def CreateMessageChennel( channelIPC : ChannelIPC , channelType : E_CHANNEL_TYPE ):
        from common_lib.MessageQueue.MessageQueueDef import MessageQueueDef
        return MessageQueueDef.MessageChannelFactoryMeta.FactoryMethod(
            channelIPC.GetIpcType()
        ).Invoke(channelIPC.GetIPC() , channelIPC.GetChannelName() , channelType  )

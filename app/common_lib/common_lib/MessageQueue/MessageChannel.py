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
    pass


class MessageChannelFactory:

    @staticmethod
    def CreateMessageChennel( channelIPC : ChannelIPC , channelType : E_CHANNEL_TYPE ):
        from common_lib.MessageQueue.MessageQueueDef import MessageQueueDef
        return MessageQueueDef.MessageChannelFactoryMeta.FactoryMethod(
            channelIPC.GetIpcType()
        ).Invoke(channelIPC.GetIPC() , channelIPC.GetChannelName() , channelType  )


#
#
# class MessageChannel:
#
#     def __init__(self,
#                  channel_nm,
#                  channel_type):
#
#         self._messageChannelContainer = None
#
#         self._channelNm = channel_nm
#         self._channelType = channel_type
#
#         from common_lib.Collections.cDict import cDict
#         # self._pipeContainer = cDict()
#
#         from common_lib.MessageQueue.PipeController import PipeController
#         self._pipeController = PipeController()
#
#         # self._init()
#
#         pass
#
#     def Build(self, message_channel_container):
#         self.SetMessageChannelContainer(message_channel_container)
#         self._init()
#         return self
#
#     def _init(self):
#
#         from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
#         from common_lib.MessageQueue.MessagePipe import MessagePipe
#         self._pipeController.Register(
#             {
#                 E_PIPE_TYPE.IN:
#                 MessagePipe(self, E_PIPE_TYPE.IN),
#                 E_PIPE_TYPE.OUT:
#                 MessagePipe(self, E_PIPE_TYPE.OUT),
#             }
#         )
#         pass
#
#     def GetPipeContainer(self):
#         return self._pipeContainer
#
#     def _getPipe(self, protocol_dir):
#
#         ## Server Type 이면 Send 는 Out
#         ## Server Type 이면 Recv 는 IN
#
#         ## Client Type 이면 Send 는 In
#         ## Client Type 이면 Recv 는 Out
#         from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
#         from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
#         if self._channelType == E_CHANNEL_TYPE.SERVER:
#
#             if protocol_dir == E_PROTOCOL_DIR.RECV:
#
#                 return self._getPipeByPipeType(E_PIPE_TYPE.IN)
#             else:
#                 return self._getPipeByPipeType(E_PIPE_TYPE.OUT)
#         else:
#             if protocol_dir == E_PROTOCOL_DIR.RECV:
#                 return self._getPipeByPipeType(E_PIPE_TYPE.OUT)
#             else:
#                 return self._getPipeByPipeType(E_PIPE_TYPE.IN)
#
#     def _getPipeByPipeType(self, pipe_type):
#         return self._pipeContainer.Get(pipe_type)
#
#     def GetChannelType(self):
#         return self._channelType
#
#     def SetMessageChannelContainer(self,
#                                    messageChannelContainer):
#         self._messageChannelContainer = messageChannelContainer
#
#     def GetChannelName(self):
#         return self._channelNm
#
#     def GetMessageQueue(self):
#         return self._messageChannelContainer.GetMessageQueue()
#
#     def Push(self, protocol):
#         from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
#
#         # print("pu")
#
#         self._getPipe(E_PROTOCOL_DIR.SEND).Push(protocol)
#
#     def Pop(self):
#         from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
#
#         # print("get==================")
#         return self._getPipe(E_PROTOCOL_DIR.RECV).Pop()
#
#     def Peek(self):
#         from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
#         return self._getPipe(E_PROTOCOL_DIR.RECV).Peek()
#
#     def Count(self):
#         from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
#         return self._getPipe(E_PROTOCOL_DIR.RECV).Count()
#
#     pass

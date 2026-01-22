from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE


class MessageChannel:

    def __init__(self,
                 channel_nm,
                 channel_type):

        self._messageChannelContainer = None

        self._channelNm = channel_nm
        self._channelType = channel_type

        from common_lib.Collections.cDict import cDict
        self._pipeContainer = cDict()
        # self._init()

        pass

    def Build(self, message_channel_container):
        self.SetMessageChannelContainer(message_channel_container)
        self._init()
        return self

    def _init(self):

        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        from common_lib.MessageQueue.MessagePipe import MessagePipe
        self._pipeContainer.Register(
            {
                E_PIPE_TYPE.IN:
                MessagePipe(self, E_PIPE_TYPE.IN),
                E_PIPE_TYPE.OUT:
                MessagePipe(self, E_PIPE_TYPE.OUT),
            }
        )
        pass

    def GetPipeContainer(self):
        return self._pipeContainer

    def _getPipe(self, protocol_dir):

        ## Server Type 이면 Send 는 Out
        ## Server Type 이면 Recv 는 IN

        ## Client Type 이면 Send 는 In
        ## Client Type 이면 Recv 는 Out
        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
        if self._channelType == E_CHANNEL_TYPE.SERVER:

            if protocol_dir == E_PROTOCOL_DIR.RECV:

                return self._getPipeByPipeType(E_PIPE_TYPE.IN)
            else:
                return self._getPipeByPipeType(E_PIPE_TYPE.OUT)
        else:
            if protocol_dir == E_PROTOCOL_DIR.RECV:
                return self._getPipeByPipeType(E_PIPE_TYPE.OUT)
            else:
                return self._getPipeByPipeType(E_PIPE_TYPE.IN)

    def _getPipeByPipeType(self, pipe_type):
        return self._pipeContainer.Get(pipe_type)

    def GetChannelType(self):
        return self._channelType

    def SetMessageChannelContainer(self,
                                   messageChannelContainer):
        self._messageChannelContainer = messageChannelContainer

    def GetChannelName(self):
        return self._channelNm

    def GetMessageQueue(self):
        return self._messageChannelContainer.GetMessageQueue()

    def Push(self, protocol):
        from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR

        # print("pu")

        self._getPipe(E_PROTOCOL_DIR.SEND).Push(protocol)

    def Pop(self):
        from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR

        # print("get==================")
        return self._getPipe(E_PROTOCOL_DIR.RECV).Pop()

    def Peek(self):
        from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
        return self._getPipe(E_PROTOCOL_DIR.RECV).Peek()

    def Count(self):
        from common_lib.MessageQueue.PipeType import E_PROTOCOL_DIR
        return self._getPipe(E_PROTOCOL_DIR.RECV).Count()

    pass

from common_lib.MessageQueue.MessageChannel import MessageChannel


class MessagePipe(object):


    def __init__(self,
                 message_channel: MessageChannel,
                 pipe_type):

        self._messageChannel = message_channel
        self._pipeType = pipe_type
        self._channelName = self._messageChannel.GetChannelName()
        self._messageQueue = self._messageChannel.GetMessageQueue()

        # self._lock = self._messageQueue.InitLock(self.GetPipeName())

        pass

    def GetPipeName(self):
        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        channelBoundStr = E_PIPE_TYPE.GetName(self._pipeType)

        return self._messageChannel.GetChannelName() + "_" + channelBoundStr

    def Push(self, protocol):
        self._messageQueue.Push(self.GetPipeName(), protocol)

    def Pop(self):
        return self._messageQueue.Pop(self.GetPipeName())

    def Peek(self):
        return self._messageQueue.Peek(self.GetPipeName())

    def Count(self):
        return self._messageQueue.Count(self.GetPipeName())

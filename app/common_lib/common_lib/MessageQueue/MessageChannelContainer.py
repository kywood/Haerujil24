from common_lib.MessageQueue.MessageQueue import IMessageQueue


class MessageChannelContainer:
    def __init__(self,
                 message_queue: IMessageQueue):
        self.message_queue = message_queue
        from common_lib.Collections.cDict import cDict
        self._messageChannelContainer = cDict()  ## channel_nm : cMessageChannel
        pass

    def _getChannel(self, channel_nm):

        if self._messageChannelContainer.IsContainKey(channel_nm) is True:
            return self._messageChannelContainer.Get(channel_nm)

        from common_lib.MessageQueue.MessageChannel import MessageChannel
        self._messageChannelContainer[channel_nm] = MessageChannel(self, channel_nm)

        return self._messageChannelContainer.Get(channel_nm)

    def GetMessageQueue(self):
        return self.message_queue

    def IsContainChannel(self, channel_name, channel_type):

        if self._messageChannelContainer.IsContainKey(channel_name):
            channel = self._messageChannelContainer.Get(channel_name)
            if channel_type == channel.GetChannelType():
                return True
        return False

    def AppendChannel(self, channel):
        self._messageChannelContainer.Put(channel.GetChannelName(), channel)
        channel.SetMessageChannelContainer(self)

    def GetChannel(self, channel_name):
        return self._messageChannelContainer.Get(channel_name)

    def Push(self, channel_nm, protocol):
        messageChannel = self._getChannel(channel_nm)
        messageChannel.Push(protocol)
        pass

    def Pop(self, channel_nm):
        messageChannel = self._getChannel(channel_nm)
        return messageChannel.Pop()

    def Peek(self, channel_nm):
        messageChannel = self._getChannel(channel_nm)
        return messageChannel.Peek()

    def Count(self, channel_nm):
        messageChannel = self._getChannel(channel_nm)
        return messageChannel.Count()

    pass
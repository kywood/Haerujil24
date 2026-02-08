from common_lib.Collections.cDict import cDict
from common_lib.MessageQueue.EventBus import EventBus
from common_lib.MessageQueue.MessageChannel import IMessageChannel


class MessageChannelController(cDict):
    def __init__(self,
                 # message_queue: IMessageQueue ,
                 event_bus : EventBus = None):
        super().__init__()
        self._event_bus = event_bus
        pass


    def IsContainChannel(self, channel_name, channel_type):

        if self.IsContainKey(channel_name):
            channel = self.Get(channel_name)
            if channel_type == channel.GetChannelType():
                return True
        return False

    def AppendMessageChannel(self, message_channel :IMessageChannel):

        self.Put(message_channel.GetChannelName(), message_channel)
        message_channel.SetMessageChannelController(self)

    def GetMessageChannel(self, channel_name) -> IMessageChannel:
        return self.Get(channel_name)
    #

    pass
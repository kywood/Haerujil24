from common_lib.Dtos.IDto import IDTO
from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE
from common_lib.MessageQueue.QueueType import E_QUEUE_TYPE


class ChannelDTO(IDTO):

    def __init__(self,
                 channel_name: str,
                 channel_type: E_CHANNEL_TYPE):
        super().__init__()
        self.channel_name = channel_name
        self.channel_type = channel_type
        pass


class ChannelQueueDTO(ChannelDTO):

    def __init__(self ,
                 channel_name : str ,
                 queue_type :E_QUEUE_TYPE ):
        super().__init__( channel_name=channel_name ,
                          channel_type=E_CHANNEL_TYPE.NONE )
        self.queueType=queue_type

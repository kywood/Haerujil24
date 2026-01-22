from common_lib.Dtos.IDto import IDTO
from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE


class ChannelDTO(IDTO):

    def __init__(self,
                 channel_name: str,
                 channel_type: E_CHANNEL_TYPE):
        super().__init__()
        self.channel_name = channel_name
        self.channel_type = channel_type
        pass



    pass
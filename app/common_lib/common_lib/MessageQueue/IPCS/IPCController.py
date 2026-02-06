from typing import List
from common_lib.Dtos.IDto import IDTO


class ChannelIPC(IDTO):

    def __init__(self , ipc , channel_name : str ):
        super().__init__()
        self._ipc = ipc
        self._channel_name = channel_name

    def GetIPC(self):
        return self._ipc

    def GetChannelName(self):
        return self._channel_name

    def GetIpcType(self):
        return self._ipc.GetIpcType()


class IPC_Controller(List):

    def __init__(self  ):
        super().__init__()

    def Append(self, ipc : ChannelIPC ):
        self.append(ipc)
        return self


    def GetChannelIPC(self , channel_name ):

        for channelIpc in self:

            if channelIpc.GetChannelName() is channel_name:
                return channelIpc

        return None

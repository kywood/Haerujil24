from typing import List

from common_lib.Dtos.IDto import IDTO


class MessageChannelDTO(IDTO):



    def __init__(self , ipc , channel_name : str ):
        super().__init__()
        self._ipc = ipc
        self._channel_name = channel_name

        pass

    def GetIPC(self):
        return self._ipc

    def GetChannelName(self):
        return self._channel_name


class MessageChennelDTOContainer(IDTO,List):

    def __init__(self):
        super().__init__()
        # self._container = []

    def Append(self , messageChannelDTO : MessageChannelDTO ):
        self.append(messageChannelDTO)

        return self
        # self._container.append(messageChannelDTO)
    #
    # def GetContainer(self):
    #     return self._container



# def main():
#     aa=MessageChennelDTOs()
#
#     mm =0
#     aa.Append(  mm )
#
#     for m in aa:
#         pass
#
#     pass
#
# if __name__ == '__main__':
#     main()


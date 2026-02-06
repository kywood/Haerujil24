from common_lib.Enum.IENUM import IENUM


class E_PIPE_TYPE(IENUM):

    SERVER_TO_CLIENT = 0
    CLIENT_TO_SERVER = 1

    COM_TO_COM = 2

    _name_map = {
        SERVER_TO_CLIENT: 'SERVER_TO_CLIENT',
        CLIENT_TO_SERVER: 'CLIENT_TO_SERVER',
        COM_TO_COM: 'COM_TO_COM',
    }

    @classmethod
    def GetName(cls, value):
        return cls._name_map.get(value, "UNKNOWN")

    @staticmethod
    def GetChannelName(channel_name , pipe_type ):
        return channel_name + "_" + E_PIPE_TYPE.GetName(pipe_type)

class E_PROTOCOL_DIR(IENUM):

    SEND = 0
    RECV = 1

    _name_map = {
        SEND: 'SEND',
        RECV: 'RECV',
    }

    @classmethod
    def GetName(cls, value):
        return cls._name.get(value, "UNKNOWN")


#
#
#
# def main():
#
#     print( E_PIPE_TYPE.GetName(E_PIPE_TYPE.IN) )
#
#     pass
#
#
# if __name__ == '__main__':
#     main()
from common_lib.Enum.IENUM import IENUM


class E_PIPE_TYPE(IENUM):

    IN = 0
    OUT = 1

    _name_map = {
        IN: 'IN',
        OUT: 'OUT',
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

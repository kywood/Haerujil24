from common_lib.Enum.IENUM import IENUM


class E_CHANNEL_TYPE(IENUM):

    NONE =  -1
    SERVER = 0
    CLIENT = 1

    _name_map = {
        NONE: 'None',
        SERVER: 'Server',
        CLIENT: 'Client',
    }

    @classmethod
    def GetName(cls, value):
        return cls._name_map.get(value, "UNKNOWN")
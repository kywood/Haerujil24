from common_lib.Enum.IENUM import IENUM


class E_CHANNEL_TYPE(IENUM):

    SERVER = 0
    CLIENT = 1

    _name_map = {
        SERVER: 'Server',
        CLIENT: 'Client',
    }

    @classmethod
    def GetName(cls, value):
        return cls._name_map.get(value, "UNKNOWN")
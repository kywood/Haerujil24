import multiprocessing

from common_lib.CallBack.CallBack import Func
from common_lib.Enum.IENUM import IENUM


class E_QUEUE_TYPE(IENUM):

    NONE =  -1
    QUEUE = 0
    HSET  = 1

    _name_map = {
        NONE: 'None',
        QUEUE: 'Queue',
        HSET: 'HSet',
    }

    _factory_map = {
        QUEUE: Func( lambda : multiprocessing.Queue() ) ,
        HSET: Func( lambda: multiprocessing.Manager().dict()),
    }

    @classmethod
    def GetName(cls, value):
        return cls._name_map.get(value, "UNKNOWN")

    @staticmethod
    def CreateQueue( e_queue_type ):
        return E_QUEUE_TYPE._factory_map.get(e_queue_type).Invoke()


#
# def main():
#     q=E_QUEUE_TYPE.CreateQueue(E_QUEUE_TYPE.QUEUE)
#
#     p=0
#
#     pass
#
#
# if __name__ == '__main__':
#     main()
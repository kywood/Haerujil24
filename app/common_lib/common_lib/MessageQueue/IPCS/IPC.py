from abc import ABC, abstractmethod

from common_lib.Enum.IENUM import IENUM
from common_lib.MessageQueue.PipeType import E_PIPE_TYPE


class IPC(ABC):


    class E_IPC_TYPE(IENUM):

        QUEUE = "QUEUE"
        HSET  = "HSET"

        pass

    def __init__(self , ipc_type :  E_IPC_TYPE ):
        self._type = ipc_type
        self._message_channel = None
        # self._pipeController = None


        self._ipc_sockets = {}
        self._ipc_sockets_locks = {}


        self._InitSocket_()

    @abstractmethod
    def _InitSocket_(self):

        pass

    def _SetSocket(self , socket_name , object ):
        self._ipc_sockets[ socket_name ] = object
        pass

    def _GetSocket(self ,socket_name ):
        return self._ipc_sockets[ socket_name ]

    def _SetSocketLock(self , socket_name ):

        from multiprocessing import  Lock
        self._ipc_sockets_locks[ socket_name ] = Lock()

    def _GetSocketLock(self , socket_name ):
        return self._ipc_sockets_locks[ socket_name ]


    def SetMessageChannel(self , message_channel ):
        self._message_channel = message_channel

    def GetIpcType(self):
        return self._type

    # def GetChannelName(self):
    #     return self._message_channel.GetChannelName()

    def GetMessageChannel(self):
        return self._message_channel


class IPC_Queue(IPC):

    def __init__(self):
        super().__init__(IPC.E_IPC_TYPE.QUEUE)
        # from common_lib.MessageQueue.PipeController import PipeController
        # self._pipeController = PipeController(self)

    def _InitSocket_(self):
        self._ipc_sockets = {}
        self._ipc_sockets_locks = {}

        from multiprocessing import Queue, Lock, Manager
        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE

        self._SetSocket(E_PIPE_TYPE.GetName(E_PIPE_TYPE.SERVER_TO_CLIENT),Queue())
        self._SetSocket(E_PIPE_TYPE.GetName(E_PIPE_TYPE.CLIENT_TO_SERVER), Queue())

        self._SetSocketLock(E_PIPE_TYPE.GetName(E_PIPE_TYPE.SERVER_TO_CLIENT))
        self._SetSocketLock(E_PIPE_TYPE.GetName(E_PIPE_TYPE.CLIENT_TO_SERVER))


    def Push(self, pipe_type : E_PIPE_TYPE , protocol):

        socket = self._GetSocket( E_PIPE_TYPE.GetName( pipe_type )  )
        socket.put( protocol )

        pass

    def Pop(self , pipe_type : E_PIPE_TYPE ,):
        socket = self._GetSocket( E_PIPE_TYPE.GetName( pipe_type )  )

        from queue import Empty
        value = None

        try:
            value = socket.get(block=False)
        except Empty:
            value = None

        return value

    def Peek(self):
        pass

    def Count(self):
        pass

    def InitLock(self):
        pass

class IPC_HSet(IPC):


    def __init__(self):
        super().__init__(IPC.E_IPC_TYPE.HSET)

        pass

    def _InitSocket_(self):
        from multiprocessing import Manager
        from multiprocessing import Lock

        self._ipc_socket = Manager().dict()
        self._ipc_socket_locks = Lock()


    def _getSocket(self):
        return self._ipc_socket

    def _getSocketLock(self):
        return self._ipc_socket_locks

    def GetHSetSocket(self):
        return self._ipc_socket

    def Set(self , key , value ):

        with self._ipc_socket_locks:
            self._getSocket()[ key ] = value

    def Get(self , key ):

        with self._ipc_socket_locks:
            return self._getSocket()[key]

    def Clear(self):

        from multiprocessing import Manager
        with self._ipc_socket_locks:
            self._ipc_socket = Manager().dict()

    def IsContain(self ,key):
        with self._ipc_socket_locks:
            return key in self._getSocket()

    def InitLock(self, channel_name):
        pass

    pass







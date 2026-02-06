from abc import abstractmethod, ABC


class IMessageHandler:
    def __init__(self):
        pass


    @abstractmethod
    def ProtocolHandle(self , protocol):
        pass

    @abstractmethod
    def SetParentProcess(self , parent_process  ):

        pass

    @abstractmethod
    def GetParentProcess(self ):

        pass


    pass

class abMessageHandler(IMessageHandler , ABC ):

    def __init__(self):
        super().__init__()
        from common_lib.Collections.cDict import cDict
        self._handlerLists = cDict()  ## protocolID, tuple

        self._parent_process = None

        #
        # self._handlerLists.Register(
        #     {
        #         "p1": (lambda pak : print(1),
        #                lambda pak : print(1),
        #                lambda pak : print(1)),
        #         "p2": (lambda pak : print(1),
        #                lambda pak : print(1),
        #                lambda pak : print(1)),
        #     }
        # )

    def GetHandler(self, protocol_id):
        if self._handlerLists.IsContainKey(protocol_id):
            return self._handlerLists.Get(protocol_id)
        else:
            return None

    def Register(self, handlers: dict):
        self._handlerLists.Register(handlers)

    @abstractmethod
    def ProtocolHandle(self , protocol):
        print(f"abMessageHandler :: {protocol}")
        pass


    def SetParentProcess(self , parent_process  ):
        self._parent_process = parent_process
        pass

    def GetParentProcess(self ):
        return self._parent_process


class MessageHandler(abMessageHandler):

    def __init__(self):
        super().__init__()

    def ProtocolHandle(self , protocol):

        process = self.GetParentProcess()
        processName = process.GetName()
        print( f"MessageHandler parentProcessNM : {processName}  [Recv]  {protocol}" )
        pass

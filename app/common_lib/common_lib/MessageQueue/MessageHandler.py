
class IMessageHandler:
    def __init__(self):
        pass

    pass

class MessageHandler(IMessageHandler):

    def __init__(self):
        super().__init__()
        from common_lib.Collections.cDict import cDict
        self._handlerLists = cDict()  ## protocolID, tuple
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
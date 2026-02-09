from common_lib.MessageQueue.MessageHandler import abMessageHandler


class MessageHandler(abMessageHandler):

    def __init__(self):
        super().__init__()

    def ProtocolHandle(self , protocol):

        process = self.GetParentProcess()
        processName = process.GetName()
        print( f"MessageHandler parentProcessNM : {processName}  [Recv]  {protocol}" )
        pass

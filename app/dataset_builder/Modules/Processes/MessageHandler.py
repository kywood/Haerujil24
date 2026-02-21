import time

from common_lib.MessageQueue.MessageHandler import abMessageHandler


class MessageHandler(abMessageHandler):

    def __init__(self):
        super().__init__()

    def ProtocolHandle(self , protocol):

        process = self.GetParentProcess()
        processName = process.GetName()
        print( f"MessageHandler parentProcessNM : {processName}  [Recv]  {protocol}" )

        time.sleep(0.3)
        pass


class WorkerMessageHandler(MessageHandler):


    def ProtocolHandle(self , protocol):

        process = self.GetParentProcess()
        processName = process.GetName()
        # print( f"MessageHandler parentProcessNM : {processName}  [Recv]  {protocol}" )

        jobProtocol = protocol


        from Defines.Defines import Defines
        messageChannelSet = process.GetEventBus().GetMessageChannel(Defines.E_IPC.MAKE_SET)

        jobMarkProtocol = messageChannelSet.Get(jobProtocol.file_path)
        print(f"WorkerMessageHandler :: {jobMarkProtocol.file_path} {jobMarkProtocol.job_state}" )

        time.sleep(5)

        jobMarkProtocol.SetComplete()

        messageChannelSet.Set(jobProtocol.file_path , jobMarkProtocol )

        time.sleep(0.3)
        pass
    pass
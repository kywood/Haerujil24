from Modules.App.App import abApp


class BuilderApp(abApp):

    def __init__(self , workerCount = 5 ):
        super().__init__()

        # self._ipcController = None

        self._multiProcess = None
        self._workerCount = workerCount

        pass


    def preProcessing(self):
        from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
        from common_lib.MessageQueue.IPCS.IPCController import ChannelIPC
        from common_lib.MessageQueue.IPCS.IPC import IPC_Queue
        from Defines.Defines import Defines
        from common_lib.MessageQueue.IPCS.IPC import IPC_HSet

        ipcController = IPC_Controller().Append(
            ChannelIPC(
                ipc=IPC_Queue(),
                channel_name=Defines.E_IPC.JOB_QUEUE
            )
        ).Append(
            ChannelIPC(
                ipc=IPC_HSet(),
                channel_name=Defines.E_IPC.MAKE_SET
            )
        )

        from common_lib.multiProcess.MultiProcesser import MultiProcesser
        self._multiProcess = MultiProcesser(ipcController)
        self._multiProcess.Init()

        from Factory.ProcessFactory import ProcessFactory
        from Modules.Processes.MessageHandler import MessageHandler

        from Defines.StateDefine import StateFactory
        from Defines.StateDefine import StateDefaine
        # stateControllerConsumer = StateFactory.CreateStateController(state_type=StateDefaine.E_StateType.Consumer )
        # stateControllerWorker = StateFactory.CreateStateController(state_type=StateDefaine.E_StateType.Worker )


        consumerProcess = ProcessFactory.CreateConsumerProcess(ipcController=ipcController,
                                                               messageHandler=MessageHandler())

        workerProcessLists = ProcessFactory.CreateWorkerProcesss(ipcController=ipcController,
                                                                 messageHandler=MessageHandler(), process_count=self._workerCount)

        self._multiProcess.Append(
            consumerProcess
        ).AppendLists(
            workerProcessLists
        )

        self._multiProcess.Start()

        pass

    def processing(self):
        pass


    def postProcessing(self):
        pass




    pass
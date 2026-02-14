




def main2():
    from common_lib.Path.BasePath import BasePath
    from Defines.Defines import Defines
    from common_lib.Config.ConfigLoader import ConfigLoader

    config_file = BasePath.instance().File(Defines.CONFIG_FILE_NAME)
    configLoader = ConfigLoader.instance(config_file)


    pass

def main():

    from common_lib.MessageQueue.IPCS.IPC import IPC_Queue
    from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
    from common_lib.MessageQueue.IPCS.IPCController import ChannelIPC
    from common_lib.MessageQueue.IPCS.IPC import IPC_HSet

    from Defines.Defines import Defines
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
    mp = MultiProcesser(ipcController)
    mp.Init()

    from Modules.Processes.MessageHandler import MessageHandler
    from Factory.ProcessFactory import ProcessFactory

    consumerProcess = ProcessFactory.CreateConsumerProcess(ipcController , MessageHandler())

    workerProcessLists = ProcessFactory.CreateWorkerProcesss(ipcController=ipcController ,messageHandler=MessageHandler() ,process_count=1)

    mp.Append(
        consumerProcess
    ).AppendLists(
        workerProcessLists
    )

    mp.Start()

    pass




if __name__ == '__main__':
    main()



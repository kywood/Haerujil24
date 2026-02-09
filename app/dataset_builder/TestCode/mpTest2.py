from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE
from common_lib.MessageQueue.IPCS.IPC import IPC_HSet


def main():

    from common_lib.MessageQueue.IPCS.IPC import IPC_Queue
    from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller
    from common_lib.MessageQueue.IPCS.IPCController import ChannelIPC

    ipcController = IPC_Controller().Append(
        ChannelIPC(
            ipc=IPC_Queue(),
            channel_name="COMQ"
        )
    ).Append(
        ChannelIPC(
            ipc=IPC_HSet(),
            channel_name="COMSet"
        )
    )

    from common_lib.multiProcess.MultiProcesser import MultiProcesser
    mp = MultiProcesser(ipcController)
    mp.Init()

    from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    from common_lib.TestCode.testProcess import cProducerProcess
    from common_lib.MessageQueue.MessageHandler import MessageHandler
    from common_lib.TestCode.testProcess import cConsumerProcess

    mp.Append(
        cProducerProcess(
            name="p1" ,
            ipcController=ipcController,
            channelDtos=[
               ChannelDTO(
                   channel_name="COMQ",
                   channel_type=E_CHANNEL_TYPE.SERVER
               ),
               ChannelDTO(
                   channel_name="COMSet",
                   channel_type=E_CHANNEL_TYPE.NONE
               )
            ],
            messageHandler=MessageHandler()
            )
    ).Append(

        cConsumerProcess(
            name="c1",
            ipcController=ipcController,
             channelDtos=[
                 ChannelDTO(
                     channel_name="COMQ",
                     channel_type=E_CHANNEL_TYPE.CLIENT
                 ),
                 ChannelDTO(
                     channel_name="COMSet"
                 )
             ],
             messageHandler=MessageHandler()
             )
    ).Append(

        cConsumerProcess(
            name="c2",
            ipcController=ipcController,
             channelDtos=[
                 ChannelDTO(
                     channel_name="COMQ",
                     channel_type=E_CHANNEL_TYPE.CLIENT
                 ),
                 ChannelDTO(
                     channel_name="COMSet"
                 )
             ],
             messageHandler=MessageHandler()
             )
    ).Append(

        cConsumerProcess(
            name="c3",
            ipcController=ipcController,
             channelDtos=[
                 ChannelDTO(
                     channel_name="COMQ",
                     channel_type=E_CHANNEL_TYPE.CLIENT
                 ),
                 ChannelDTO(
                     channel_name="COMSet"
                 )
             ],
             messageHandler=MessageHandler()
             )
    )

    mp.Start()


if __name__ == '__main__':
    main()
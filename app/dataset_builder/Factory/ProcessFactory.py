from common_lib.CallBack.CallBack import Func
from common_lib.Enum.IENUM import IENUM
from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE

from Defines.Defines import Defines
from Factory.Factory import IFactory
from Modules.Processes.ConsumerProcess import ConsumerProcess
from Modules.Processes.WorkerProcess import WorkerProcess


class ProcessFactory(IFactory):

    class E_PROCESS_TYPE(IENUM):
        CONSUMER_PROCESS = "ConsumerProcess"
        WORKER_PROCESS = "WorkerProcess"


    factories = {
        E_PROCESS_TYPE.CONSUMER_PROCESS: Func( lambda ipcController , messageHandler : ConsumerProcess(
                                                                                name="ConsumerProcess" ,
                                                                                ipcController=ipcController ,
                                                                                channelDtos=[
                                                                                    ChannelDTO(
                                                                                        channel_name=Defines.E_IPC.JOB_QUEUE,
                                                                                        channel_type=E_CHANNEL_TYPE.SERVER
                                                                                    ),
                                                                                    ChannelDTO(
                                                                                        channel_name=Defines.E_IPC.MAKE_SET,
                                                                                    )
                                                                                ],
                                                                                messageHandler=messageHandler
                                                                              ) ),
        E_PROCESS_TYPE.WORKER_PROCESS: Func( lambda  ipcController , process_name ,messageHandler : WorkerProcess(
                                                                                name=process_name,
                                                                                ipcController=ipcController,
                                                                                channelDtos=[
                                                                                    ChannelDTO(
                                                                                        channel_name=Defines.E_IPC.JOB_QUEUE,
                                                                                        channel_type=E_CHANNEL_TYPE.CLIENT
                                                                                    ),
                                                                                    ChannelDTO(
                                                                                        channel_name=Defines.E_IPC.MAKE_SET,
                                                                                    )
                                                                                ],
                                                                                messageHandler=messageHandler
                                                                            ) )
    }

    @staticmethod
    def CreateConsumerProcess( ipcController ,messageHandler ):
        return ProcessFactory.factories[ProcessFactory.E_PROCESS_TYPE.CONSUMER_PROCESS].Invoke(ipcController ,messageHandler)

    @staticmethod
    def CreateWorkerProcesss(  ipcController , messageHandler , process_count ):

        processLists=[]

        for loopCnt in range( process_count ):
            process_no = loopCnt + 1

            processName= f"WorkerProcess_{process_no}"

            processLists.append(
                ProcessFactory.factories[ProcessFactory.E_PROCESS_TYPE.WORKER_PROCESS].Invoke(
                    ipcController, processName , messageHandler
                )
            )

        return processLists

    pass

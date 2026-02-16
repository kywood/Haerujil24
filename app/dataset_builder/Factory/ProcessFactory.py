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
        E_PROCESS_TYPE.CONSUMER_PROCESS: Func( lambda ipcController, stateControllerWorker , messageHandler : ConsumerProcess(
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
                                                                                messageHandler=messageHandler,
                                                                                stateController=stateControllerWorker

                                                                              ) ),
        E_PROCESS_TYPE.WORKER_PROCESS: Func( lambda  ipcController , stateControllerWorker, process_name ,messageHandler : WorkerProcess(
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
                                                                                messageHandler=messageHandler,
                                                                                stateController=stateControllerWorker
                                                                            ) )
    }

    @staticmethod
    def CreateConsumerProcess( ipcController , messageHandler ):
        from Defines.StateDefine import StateDefine
        from Defines.StateFactory import StateFactory

        stateController = StateFactory.CreateStateController(state_type=StateDefine.E_StateType.Consumer)
        # process = ProcessFactory.factories[ProcessFactory.E_PROCESS_TYPE.CONSUMER_PROCESS].Invoke(ipcController , stateController ,messageHandler)

        # process.With

        return ProcessFactory.factories[ProcessFactory.E_PROCESS_TYPE.CONSUMER_PROCESS].Invoke(ipcController , stateController ,messageHandler)

    @staticmethod
    def CreateWorkerProcesss(  ipcController ,  messageHandler , process_count ):

        processLists=[]

        from Defines.StateDefine import StateDefine
        from Defines.StateFactory import StateFactory

        for loopCnt in range( process_count ):
            process_no = loopCnt + 1

            processName= f"WorkerProcess_{process_no}"

            stateControllerWorker = StateFactory.CreateStateController(state_type=StateDefine.E_StateType.Worker)

            processLists.append(
                ProcessFactory.factories[ProcessFactory.E_PROCESS_TYPE.WORKER_PROCESS].Invoke(
                    ipcController, stateControllerWorker, processName , messageHandler
                )
            )

        return processLists

    pass

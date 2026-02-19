import time
from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller

from Modules.Processes.ConfigEventBusProcess import ConfigEventBusProcess
from Modules.Processes.MessageHandler import MessageHandler
from Modules.Processes.StateProcess import StateProcess
from Modules.State.StateController import StateController

class WorkerProcess(ConfigEventBusProcess , StateProcess):


    def __init__(self,
                 ipcController: IPC_Controller,
                 channelDtos: List[ChannelDTO],
                 messageHandler: MessageHandler,
                 stateController: StateController = None ,
                 name: str = "None"
                 ):
        ConfigEventBusProcess.__init__( self, ipcController=ipcController ,
                                        channelDtos=channelDtos,
                                        messageHandler=messageHandler,
                                        name=name
                                        )
        StateProcess.__init__(self ,stateController=stateController)


    def WithStateController(self ,stateController : StateController  ):

        super().WithStateController(stateController )

        from Defines.StateDefine import StateDefine
        self._getStateController().ChangeState(StateDefine.WorkerState.E_STATE.Running)

        return self



    def ProcProcessing(self, process):
        # print("WorkerProcess::process -- call!!")

        self._getStateController().Proc()


        time.sleep(1)

        pass


    pass


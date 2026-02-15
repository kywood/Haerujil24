from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelDTO
from common_lib.MessageQueue.IPCS.IPCController import IPC_Controller

from Modules.Processes.ConfigEventBusProcess import ConfigEventBusProcess
from Modules.Processes.MessageHandler import MessageHandler
from Modules.Processes.StateProcess import StateProcess
from Modules.State.StateController import StateController


class ConsumerProcess(ConfigEventBusProcess , StateProcess):

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


        pass


    ## TODO F: 이부분은 StateContreoller 에서 초기화 스테이트를 넣자..
    def WithStateController(self ,stateController : StateController  ):

        super().WithStateController(stateController )

        from Defines.StateDefine import StateDefaine
        self._getStateController().ChangeState(StateDefaine.ConsumerState.E_STATE.Idle)

        return self



    def CallProcessing(self, process):

        print("process -- call!!")

        pass


    @staticmethod
    def CreateProcess():


        pass
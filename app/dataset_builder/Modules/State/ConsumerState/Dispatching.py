from typing import Any

from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class DispatchingState(abState):

    def __init__(self,stateController):
        super().__init__(stateController,StateDefine.ConsumerState.E_STATE.Dispatching)
        self._unNormalLists = None

    def Enter(self, stateEnterData :Any = None):
        print("DispatchingState::Enter")
        self._unNormalLists = stateEnterData
        pass


    def Leave(self):
        print("DispatchingState::Leave")
        pass


    def Proc(self):
        print(f"DispatchingState::Proc")

        ## 잡을 할당 한다...

        from Defines.Defines import Defines
        from Modules.Protocol.Protocol import JobProtocol
        from Modules.Protocol.Protocol import JobMarkProtocol
        messageChannelSet = self.GetParentProcess().GetEventBus().GetMessageChannel(Defines.E_IPC.MAKE_SET)
        # self.GetEventBus().GetMessageChannel(Defines.E_IPC.JOB_QUEUE)

        for unNormal in self._unNormalLists:
            # print(unNormal)

            self.GetParentProcess().GetEventBus().Send(Defines.E_IPC.JOB_QUEUE ,JobProtocol(file_path=unNormal) )
            # messageChannelQueue.Push(unNormal)
            messageChannelSet.Set(unNormal  ,JobMarkProtocol(file_path=unNormal) )

            pass

        self.GetStateController().ChangeState(
            state_id=StateDefine.ConsumerState.E_STATE.AwaitingCompletion
        )

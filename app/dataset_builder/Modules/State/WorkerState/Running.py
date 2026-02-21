from typing import Any

from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class RunningState(abState):


    def __init__(self,stateController):
        super().__init__(stateController , StateDefine.WorkerState.E_STATE.Running)


    def Enter(self, stateEnterData :Any = None):
        print("RunningState::Idle")
        pass


    def Leave(self):
        print("RunningState::Leave")
        pass

    def Proc(self):

        # print(f"RunningState::Proc")
        pass

    pass

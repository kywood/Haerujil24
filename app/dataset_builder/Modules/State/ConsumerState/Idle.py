from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class IdleState(abState):

    def __init__(self,):
        super().__init__(StateDefine.ConsumerState.E_STATE.Idle)

    def Enter(self):
        print("IdleState::Idle")
        pass


    def Leave(self):
        print("IdleState::Leave")
        pass

    def Proc(self):
        print(f"IdleState::Proc")
        pass

    pass
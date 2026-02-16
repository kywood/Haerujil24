from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class DispatchingState(abState):

    def __init__(self,):
        super().__init__(StateDefine.ConsumerState.E_STATE.Dispatching)

    def Enter(self):
        print("DispatchingState::Idle")
        pass


    def Leave(self):
        print("DispatchingState::Leave")
        pass


    def Proc(self):
        pass

    pass

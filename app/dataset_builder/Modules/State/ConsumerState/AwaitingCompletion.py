from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class AwaitingCompletionState(abState):


    def __init__(self):
        super().__init__(StateDefine.ConsumerState.E_STATE.AwaitingCompletion)


    def Enter(self):
        print("AwaitingCompletionState::Idle")
        pass


    def Leave(self):
        print("AwaitingCompletionState::Leave")
        pass


    def Proc(self):
        pass

    pass

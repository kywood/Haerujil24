from abc import ABC
from common_lib.Enum.IENUM import IENUM
from Defines.Defines import IDefine


class E_BaseState(IENUM):
    SNone = "None"


class StateDefine(IDefine, ABC):

    class E_StateType(IENUM):
        Consumer = "Consumer"
        Worker   = "Worker"

    class ConsumerState:
        class E_STATE(E_BaseState):
            Idle = "Idle"
            Dispatching = "Dispatching"
            AwaitingCompletion = "AwaitingCompletion"

    class WorkerState(IENUM):

        class E_STATE(E_BaseState):
            Running = "Running"



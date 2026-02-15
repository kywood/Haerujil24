from abc import ABC

from common_lib.CallBack.CallBack import Func
from common_lib.Enum.IENUM import IENUM

from Defines.Defines import IDefine
from Modules.State.ConsumerState.AwaitingCompletion import AwaitingCompletionState
from Modules.State.ConsumerState.Dispatching import DispatchingState
from Modules.State.ConsumerState.Idle import IdleState
from Modules.State.WorkerState.Running import RunningState


class E_BaseState(IENUM):
    SNone = "None"


class StateDefaine(IDefine,ABC):

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


class StateMeta:

    meta = {
        StateDefaine.E_StateType.Consumer : {
            StateDefaine.ConsumerState.E_STATE.Idle: Func(lambda: IdleState()),
            StateDefaine.ConsumerState.E_STATE.Dispatching: Func(lambda: DispatchingState()),
            StateDefaine.ConsumerState.E_STATE.AwaitingCompletion: Func(lambda: AwaitingCompletionState())
        } ,
        StateDefaine.E_StateType.Worker : {
            StateDefaine.WorkerState.E_STATE.Running: Func(lambda: RunningState()),
        }
    }


class StateFactory:

    @staticmethod
    def CreateStateController( state_type  : StateDefaine.E_StateType ):
        from Modules.State.StateController import StateController
        stateController = StateController()

        for state_id in StateMeta.meta[state_type].keys():
            stateController.AppendState(StateMeta.meta[state_type][state_id].Invoke())

        return stateController



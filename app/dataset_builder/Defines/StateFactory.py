from common_lib.CallBack.CallBack import Func

from Defines.StateDefine import StateDefine
from Modules.State.ConsumerState.AwaitingCompletion import AwaitingCompletionState
from Modules.State.ConsumerState.Dispatching import DispatchingState
from Modules.State.ConsumerState.Idle import IdleState
from Modules.State.WorkerState.Running import RunningState



class StateMeta:

    meta = {
        StateDefine.E_StateType.Consumer : {
            StateDefine.ConsumerState.E_STATE.Idle: Func(lambda: IdleState()),
            StateDefine.ConsumerState.E_STATE.Dispatching: Func(lambda: DispatchingState()),
            StateDefine.ConsumerState.E_STATE.AwaitingCompletion: Func(lambda: AwaitingCompletionState())
        } ,
        StateDefine.E_StateType.Worker : {
            StateDefine.WorkerState.E_STATE.Running: Func(lambda: RunningState()),
        }
    }


class StateFactory:

    @staticmethod
    def GetCallBack(state_type  : StateDefine.E_StateType, state_id):
        return StateMeta.meta[state_type][state_id]

    @staticmethod
    def CreateStateController(state_type  : StateDefine.E_StateType):
        from Modules.State.StateController import StateController
        stateController = StateController()

        for state_id in StateMeta.meta[state_type].keys():
            stateCallback = StateFactory.GetCallBack(state_type, state_id )
            stateController.AppendState(StateMeta.meta[state_type][state_id].Invoke())

        return stateController


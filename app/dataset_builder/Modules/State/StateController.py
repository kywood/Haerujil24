from typing import Any

from Defines.StateDefine import E_BaseState


class StateController:

    def __init__(self , parent_process = None  ):
        self._container = {}
        self._currentStateID = None

        self.SetParentProcess(parent_process)
        pass

    def AppendState(self , state ):
        self._container[ state.GetStateID() ] = state

    def SetParentProcess(self , parent_process ):
        self._parentProcess =  parent_process

    def GetParentProcess(self):
        return self._parentProcess


    def GetState(self , state_id : E_BaseState ):
        return self._container[state_id]

    def GetCurrentState(self):
        return self.GetState( self._currentStateID )

    def SetCurrnetState(self , state_id : E_BaseState ):
        self._currentStateID = state_id

    def ChangeState(self, state_id : E_BaseState , stateEnterData : Any = None):

        if self._currentStateID == None:
            nextState = self.GetState( state_id )
            nextState.Enter(stateEnterData)
        else:
            currentState = self.GetState( self._currentStateID )
            nextState = self.GetState( state_id )

            currentState.Leave()
            nextState.Enter(stateEnterData)

        self._currentStateID = state_id

    def Proc(self):
        self.GetCurrentState().Proc()
        pass


from Modules.State.StateController import StateController


class StateProcess:



    def __init__(self , stateController : StateController = None):

        self._stateController = stateController


    def WithStateController(self ,stateController : StateController  ):
        self._stateController = stateController
        return self


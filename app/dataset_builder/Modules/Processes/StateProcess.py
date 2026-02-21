from abc import abstractmethod

from Modules.State.State import abState
from Modules.State.StateController import StateController


class StateProcess:



    def __init__(self , stateController : StateController = None):

        self._stateController = stateController

        self.WithStateController(stateController)


    def WithStateController(self ,stateController : StateController ):
        self._stateController = stateController

        self._stateController.SetParentProcess(self)

        return self


    def _getStateController(self):
        return self._stateController

    # def _getCurrentState(self):
    #     return self._stateController.GetCurrentState()

    # @abstractmethod
    def ProcProcessing(self):
        # raise NotImplementedError

        self._getStateController().Proc()



        pass



from abc import abstractmethod

from Modules.JobQueue.JobQueue import JobQueue
from Modules.State.State import abState
from Modules.State.StateController import StateController


class StateProcess:



    def __init__(self , stateController : StateController = None):

        self._stateController = stateController

        self._jobQueue = None

        self.WithStateController(stateController)

    def GetJobQueue(self):
        return self._jobQueue

    def PostInit(self):
        # super().PostInit()
        # print(f" ==================== ConfigLoader {self.GetName()}")
        self._jobQueue = JobQueue()


    def WithStateController(self ,stateController : StateController ):
        self._stateController = stateController

        # self._jobQueue = JobQueue()

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



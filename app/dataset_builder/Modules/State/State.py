from abc import ABC, abstractmethod
from typing import Any


class IState(ABC):

    @abstractmethod
    def Enter(self,stateEnterData :Any = None):
        raise NotImplementedError

    @abstractmethod
    def Leave(self):
        raise NotImplementedError

    @abstractmethod
    def GetStateID(self):
        raise NotImplementedError

    @abstractmethod
    def Proc(self):
        raise NotImplementedError

    pass


class abState(IState,ABC):


    def __init__(self , stateController , state_id ):

        self._state_id = state_id
        self._stateController = stateController

        pass

    @abstractmethod
    def Enter(self , stateEnterData :Any = None):
        raise NotImplementedError

    @abstractmethod
    def Leave(self):
        raise NotImplementedError


    def GetStateID(self):
        return self._state_id

    def GetParentProcess(self):
        return self._stateController.GetParentProcess()

    def GetStateController(self):
        return self._stateController


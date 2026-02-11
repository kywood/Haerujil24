from abc import ABC, abstractmethod


class IState(ABC):

    @abstractmethod
    def Enter(self):
        raise NotImplementedError

    @abstractmethod
    def Leave(self):
        raise NotImplementedError

    @abstractmethod
    def GetStateID(self):
        raise NotImplementedError

    pass


class abState(IState,ABC):


    def __init__(self , state_id ):

        self._state_id = state_id

        pass

    @abstractmethod
    def Enter(self):
        raise NotImplementedError

    @abstractmethod
    def Leave(self):
        raise NotImplementedError


    def GetStateID(self):
        return self._state_id


    pass



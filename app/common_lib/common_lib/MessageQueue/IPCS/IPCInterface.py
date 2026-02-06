
from abc import ABC, abstractmethod

class IQueueType(ABC):


    @abstractmethod
    def Push(self , protocol):


        pass

    @abstractmethod
    def Pop(self):
        pass


    pass


class IHSetType(ABC):

    #
    # @abstractmethod
    # def Push(self , protocol):
    #
    #
    #     pass
    #
    # @abstractmethod
    # def Pop(self):
    #     pass


    pass
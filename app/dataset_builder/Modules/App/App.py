from abc import abstractmethod, ABC


class IApp(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def preProcessing(self):
        raise NotImplementedError

    @abstractmethod
    def processing(self):
        raise NotImplementedError


    @abstractmethod
    def postProcessing(self):
        raise NotImplementedError

    @abstractmethod
    def Run(self):
        raise NotImplementedError


class abApp(IApp,ABC):

    def __init__(self):
        super().__init__()

        pass

    @abstractmethod
    def preProcessing(self):
        raise NotImplementedError

    @abstractmethod
    def processing(self):
        raise NotImplementedError


    @abstractmethod
    def postProcessing(self):
        raise NotImplementedError



    def Run(self):
        self.preProcessing()

        self.processing()

        self.postProcessing()
        pass

    pass




from abc import ABC, abstractmethod
from fastapi import FastAPI


class IController(ABC):

    def __init__(self):


        pass

    @abstractmethod
    def register(self, app: FastAPI) -> None:
        """이 컨트롤러가 가진 엔드포인트들을 app에 등록"""
        raise NotImplementedError

    pass
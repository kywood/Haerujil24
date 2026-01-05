from abc import ABC, abstractmethod
from typing import Iterable, Sequence
from common_lib.ObjectStorage.ObjectStat import ObjectStat


class ObjectStorage(ABC):

    def __init__(self ):
        pass

    # listing
    @abstractmethod
    def ls(self, prefix: str = "") -> Iterable[str]:
        pass

    @abstractmethod
    def walk(self, prefix: str = "") -> Iterable[str]:
        pass

    # write
    @abstractmethod
    def puts(self, items: Sequence[tuple[str, str]]) -> None:
        """[(local_path, key), ...]"""
        pass

    # read
    @abstractmethod
    def get(self, key: str, local_path: str) -> None:
        pass

    # meta
    @abstractmethod
    def stat(self, key: str) -> ObjectStat | None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    # delete
    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def mkdir(self, key: str) -> None:
        pass

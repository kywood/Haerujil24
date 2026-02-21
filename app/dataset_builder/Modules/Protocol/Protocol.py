import dataclasses
from abc import ABC
from typing import TypeVar, Type

from Defines.ProtocolDefine import E_JOB_STATE

T = TypeVar("T", bound="abProtocol")

class IProtocol(ABC):




    pass


class abProtocol(IProtocol,ABC):

    def toJson(self):
        import json
        return json.dumps(dataclasses.asdict(self), ensure_ascii=False)

    @classmethod
    def fromJson(cls: Type[T], s: str) -> T:
        import json
        data = json.loads(s)
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON: expected an object")
        return cls(**data)  # type: ignore[misc]


    pass


@dataclasses.dataclass
class JobProtocol(abProtocol):

    file_path:str

@dataclasses.dataclass
class JobMarkProtocol(abProtocol):

    file_path : str
    job_state : str = E_JOB_STATE.PENDING

    def SetComplete(self):
        self.job_state = E_JOB_STATE.COMPLETED
        pass

    def IsComplete(self):
        return self.job_state == E_JOB_STATE.COMPLETED


#
#
# def main():
#     a = JobProtocol("kim")
#     s = a.toJson()
#
#     b = JobProtocol.fromJson(s)
#     print(b.file_path)
#
#     pass
#
#
# if __name__ == '__main__':
#     main()



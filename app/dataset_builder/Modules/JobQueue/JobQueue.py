from typing import Any, Optional
from common_lib.Collections.ICollection import ICollection

class JobQueue(ICollection):

    def __init__(self):
        super().__init__()

        from collections import deque
        self._queue = deque()

    def Push(self , job : Any):
        self._queue.append(job)

    def Pop(self) -> Optional[Any]:
        return self._queue.popleft() if self._queue else None

    def Count(self) -> int:
        return len(self._queue)

    def IsEmpty(self) -> bool:
        return len(self._queue) == 0

    def Clear(self) -> None:
        self._queue.clear()

    def Peek(self) -> Optional[Any]:
        return self._queue[0] if self._queue else None


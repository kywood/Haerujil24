from typing import Any, Optional
from common_lib.Collections.ICollection import ICollection

class JobQueue(ICollection):

    def __init__(self):
        super().__init__()

        from collections import deque
        from threading import Lock

        self._queue = deque()
        self._lock = Lock()

    def Push(self , job : Any):
        with self._lock:
            self._queue.append(job)

    def Pop(self) -> Optional[Any]:
        with self._lock:
            return self._queue.popleft() if self._queue else None

    def Count(self) -> int:
        with self._lock:
            return len(self._queue)

    def IsEmpty(self) -> bool:
        with self._lock:
            return len(self._queue) == 0

    def Clear(self) -> None:
        with self._lock:
            self._queue.clear()

    def Peek(self) -> Optional[Any]:
        with self._lock:
            return self._queue[0] if self._queue else None


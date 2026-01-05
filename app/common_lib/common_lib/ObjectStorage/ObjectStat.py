from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ObjectStat:
    key: str
    size: int
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None


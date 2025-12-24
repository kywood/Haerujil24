from abc import ABC
from typing import List, Optional, Dict, Any

from pydantic import BaseModel

class BoxModel(BaseModel):
    cls: int
    conf: float
    xyxy: List[float]  # [x1, y1, x2, y2]




class PredictResponse(BaseModel):
    model_key: str
    local_model_path: str
    image_size: List[int]  # [w, h]
    boxes: List[BoxModel]
    names: Optional[Dict[Any, Any]] = None
    latency_ms: float
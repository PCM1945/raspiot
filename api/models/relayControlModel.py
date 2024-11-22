from pydantic import BaseModel
from typing import Literal

class Relay(BaseModel):
    camera_id: int
    action: str 
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class LogCreate(BaseModel):
    device_id: str
    app_id: str
    type: str = Field(..., example="telemetry")
    data: Dict[str, Any]

class LogInDB(LogCreate):
    branch_id: str
    timestamp: datetime

class GenericLogPayload(BaseModel):
    data: Dict[str, Any]
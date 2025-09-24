from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    response: str
    stage: str
    session_active: bool
    interaction_count: int
    expires_in: str

class HealthResponse(BaseModel):
    status: str
    sessions: int
    uptime: str

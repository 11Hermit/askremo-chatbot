from pydantic import BaseModel, constr

class ChatRequest(BaseModel):
    session_id: constr(min_length=1)
    message: constr(min_length=1)

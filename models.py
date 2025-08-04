from pydantic import BaseModel, EmailStr

class Guest(BaseModel):
    email: EmailStr

class QueueStatus(BaseModel):
    is_open: bool
    queue: list[str]
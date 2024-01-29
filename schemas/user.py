from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id: str
    username: str
    email: str
    password: str 

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
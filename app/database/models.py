from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

class AdminOut(BaseModel):
    admin_id: str
    username: str

class Assignment(BaseModel):
    task: str
    admin: str
    status: Optional[str] = "pending"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
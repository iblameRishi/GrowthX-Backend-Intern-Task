from pydantic import BaseModel
from typing import Optional

# Schema for creating a user
class User(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

# Schema for returning admin info in GET /admins - make sure password isn't also sent out in data
class AdminOut(BaseModel):
    admin_id: str
    username: str

# Schema for creating an assignment
class Assignment(BaseModel):
    task: str
    admin: str
    status: Optional[str] = "pending"

# Schema for access token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    id: Optional[str] = None
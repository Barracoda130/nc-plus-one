
from datetime import datetime

from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserCreatedResponse(BaseModel):
    user: UserResponse
    
class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str
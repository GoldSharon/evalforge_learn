from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    full_name: str | None = None 
    password: str 

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:str 
    email: str
    full_name: str | None = None 
    is_active: bool
    created_at: datetime
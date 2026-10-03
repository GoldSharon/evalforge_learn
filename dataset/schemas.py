from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DatasetCreate(BaseModel):
    name: str 
    description: str 


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str 
    name: str 
    description: Optional[str] = None 
    created_at : datetime


class DatasetUpdate(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None


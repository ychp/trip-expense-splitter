from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional


class MemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="成员名称")
    trip_id: int = Field(..., description="行程ID")


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class MemberResponse(MemberBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True
    
    @field_validator('created_at', mode='before')
    @classmethod
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')
        return v

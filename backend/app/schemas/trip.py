from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, date
from typing import Optional, List, Any


class TripBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="行程名称")
    description: Optional[str] = Field(None, description="行程描述")
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    status: str = Field(default="planning", description="状态: planning/ongoing/completed")


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None


class MemberInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str


class TripResponse(TripBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: str
    updated_at: str
    members: List[MemberInfo] = []
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def format_date(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')
        return v
    
    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def format_datetime(cls, v: Any) -> str:
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')
        return v

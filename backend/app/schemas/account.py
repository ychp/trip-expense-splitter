from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="账户名称")
    type: str = Field(..., description="账户类型: cash/bank/alipay/wechat/investment")
    balance: float = Field(default=0.0, ge=0, description="账户余额")


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = None
    balance: Optional[float] = Field(None, ge=0)


class AccountResponse(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from dateutil.parser import parse


class TransactionBase(BaseModel):
    account_id: int = Field(..., description="账户ID")
    category_id: int = Field(..., description="分类ID")
    type: str = Field(..., description="类型: income/expense/transfer")
    amount: float = Field(..., gt=0, description="金额")
    transaction_date: str = Field(..., description="交易日期 (YYYY-MM-DD)")
    remark: Optional[str] = Field(None, max_length=500, description="备注")
    
    @field_validator('transaction_date')
    @classmethod
    def parse_date(cls, v):
        try:
            return str(parse(v).date())
        except:
            raise ValueError('日期格式错误,请使用 YYYY-MM-DD 格式')


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    type: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    transaction_date: Optional[str] = None
    remark: Optional[str] = Field(None, max_length=500)


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

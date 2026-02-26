from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, date
from typing import Optional, List, Dict
from dateutil.parser import parse


class CategoryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class WalletInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class MemberInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class TransactionSplitCreate(BaseModel):
    member_id: int
    amount: float
    split_method: str


class TransactionSplitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    transaction_id: int
    member_id: int
    member_name: str = ""
    amount: float
    split_method: str


class TransactionBase(BaseModel):
    trip_id: int
    wallet_id: int
    category_id: Optional[int] = None
    transaction_type: str = Field(default="expense", description="deposit/expense")
    amount: float = Field(..., gt=0)
    payer_id: Optional[int] = None
    transaction_date: str
    remark: Optional[str] = None
    
    @field_validator('transaction_date')
    @classmethod
    def parse_date(cls, v):
        try:
            return str(parse(v).date())
        except:
            raise ValueError('日期格式错误,请使用 YYYY-MM-DD 格式')


class DepositCreate(BaseModel):
    wallet_id: int
    member_id: int
    amount: float = Field(..., gt=0)
    transaction_date: str
    remark: Optional[str] = None


class ExpenseCreate(BaseModel):
    trip_id: int
    wallet_id: int
    category_id: int
    amount: float = Field(..., gt=0)
    payer_id: int
    split_method: str = Field(default="equal", description="equal/ratio/custom")
    split_members: Optional[List[int]] = None
    split_ratios: Optional[Dict[int, float]] = None
    transaction_date: str
    remark: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    wallet_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0)
    transaction_date: Optional[str] = None
    remark: Optional[str] = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: str
    wallet: Optional[WalletInfo] = None
    category: Optional[CategoryInfo] = None
    payer: Optional[MemberInfo] = None
    splits: List[TransactionSplitResponse] = []
    
    @field_validator('transaction_date', mode='before')
    @classmethod
    def format_transaction_date(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')
        return v
    
    @field_validator('created_at', mode='before')
    @classmethod
    def format_created_at(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return v


class WalletFlowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    wallet_id: int
    transaction_id: int
    member_id: int
    member_name: str = ""
    flow_type: str
    amount: float
    balance_before: float
    balance_after: float
    created_at: str
    
    @field_validator('created_at', mode='before')
    @classmethod
    def format_created_at(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return v

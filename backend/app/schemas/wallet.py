from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, date
from typing import Optional, List


class WalletMemberBase(BaseModel):
    member_id: int
    balance: float = Field(default=0, ge=0)


class WalletMemberCreate(WalletMemberBase):
    pass


class WalletMemberResponse(WalletMemberBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    wallet_id: int
    member_name: str = ""
    
    @classmethod
    def from_orm_with_name(cls, wallet_member):
        return cls(
            id=wallet_member.id,
            wallet_id=wallet_member.wallet_id,
            member_id=wallet_member.member_id,
            balance=wallet_member.balance,
            member_name=wallet_member.member.name if wallet_member.member else ""
        )


class WalletBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    trip_id: int


class WalletCreate(WalletBase):
    pass


class WalletUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class WalletResponse(WalletBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total_balance: float = 0
    created_at: str
    updated_at: str
    wallet_members: List[WalletMemberResponse] = []
    
    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')
        return v

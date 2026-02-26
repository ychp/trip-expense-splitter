from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class WalletFlowBase(BaseModel):
    wallet_id: int
    transaction_id: int
    member_id: int
    flow_type: str
    amount: float
    balance_before: float
    balance_after: float


class WalletFlowResponse(WalletFlowBase):
    id: int
    member_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MemberFlowSummary(BaseModel):
    member_id: int
    member_name: str
    deposit_amount: float
    expense_amount: float
    current_balance: float


class WalletFlowSummary(BaseModel):
    wallet_id: int
    total_deposit: float
    total_expense: float
    member_summaries: List[MemberFlowSummary]

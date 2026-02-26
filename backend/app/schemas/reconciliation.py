from pydantic import BaseModel
from typing import List, Optional


class MemberDetail(BaseModel):
    member_id: int
    member_name: str
    current_balance: float
    total_deposited: float
    total_spent: float
    share_ratio: float


class MemberSettlement(BaseModel):
    from_member_id: int
    from_member_name: str
    to_member_id: int
    to_member_name: str
    amount: float


class WalletReconciliation(BaseModel):
    wallet_id: int
    wallet_name: str
    total_balance: float
    member_count: int
    members: List[MemberDetail]
    settlements: List[MemberSettlement]


class TripSummaryMember(BaseModel):
    member_id: int
    member_name: str
    total_balance: float
    total_deposited: float
    total_spent: float


class ReconciliationReport(BaseModel):
    trip_id: int
    total_wallets: int
    overall_balance: float
    wallets: List[WalletReconciliation]
    trip_summary: List[TripSummaryMember]

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.wallet_flow import WalletFlow
from app.models.wallet_member import WalletMember
from app.models.member import Member
from app.schemas.wallet_flow import WalletFlowResponse, WalletFlowSummary

router = APIRouter()


@router.get("/", response_model=List[WalletFlowResponse])
def get_wallet_flows(
    wallet_id: Optional[int] = Query(None, description="钱包ID"),
    member_id: Optional[int] = Query(None, description="成员ID"),
    flow_type: Optional[str] = Query(None, description="流水类型: deposit_in/expense_out"),
    trip_id: Optional[int] = Query(None, description="行程ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    query = db.query(WalletFlow)
    
    if wallet_id is not None:
        query = query.filter(WalletFlow.wallet_id == wallet_id)
    
    if member_id is not None:
        query = query.filter(WalletFlow.member_id == member_id)
    
    if flow_type is not None:
        query = query.filter(WalletFlow.flow_type == flow_type)
    
    if trip_id is not None:
        from app.models.wallet import Wallet
        query = query.join(Wallet, WalletFlow.wallet_id == Wallet.id).filter(Wallet.trip_id == trip_id)
    
    flows = query.order_by(WalletFlow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for flow in flows:
        member = db.query(Member).filter(Member.id == flow.member_id).first()
        member_name = member.name if member else "未知成员"
        
        result.append({
            "id": flow.id,
            "wallet_id": flow.wallet_id,
            "transaction_id": flow.transaction_id,
            "member_id": flow.member_id,
            "member_name": member_name,
            "flow_type": flow.flow_type,
            "amount": flow.amount,
            "balance_before": flow.balance_before,
            "balance_after": flow.balance_after,
            "created_at": flow.created_at
        })
    
    return result


@router.get("/summary/{wallet_id}", response_model=WalletFlowSummary)
def get_wallet_flow_summary(
    wallet_id: int,
    db: Session = Depends(get_db)
):
    flows = db.query(WalletFlow).filter(WalletFlow.wallet_id == wallet_id).all()
    
    if not flows:
        return {
            "wallet_id": wallet_id,
            "total_deposit": 0,
            "total_expense": 0,
            "member_summaries": []
        }
    
    total_deposit = sum(f.amount for f in flows if f.flow_type == "deposit_in")
    total_expense = sum(f.amount for f in flows if f.flow_type == "expense_out")
    
    member_summaries = {}
    for flow in flows:
        if flow.member_id not in member_summaries:
            member = db.query(Member).filter(Member.id == flow.member_id).first()
            member_summaries[flow.member_id] = {
                "member_id": flow.member_id,
                "member_name": member.name if member else "未知成员",
                "deposit_amount": 0,
                "expense_amount": 0,
                "current_balance": 0
            }
        
        if flow.flow_type == "deposit_in":
            member_summaries[flow.member_id]["deposit_amount"] += flow.amount
        elif flow.flow_type == "expense_out":
            member_summaries[flow.member_id]["expense_amount"] += flow.amount
        
        member_summaries[flow.member_id]["current_balance"] = flow.balance_after
    
    return {
        "wallet_id": wallet_id,
        "total_deposit": total_deposit,
        "total_expense": total_expense,
        "member_summaries": list(member_summaries.values())
    }


@router.get("/member/{member_id}", response_model=List[WalletFlowResponse])
def get_member_flows(
    member_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    flows = db.query(WalletFlow).filter(WalletFlow.member_id == member_id).order_by(
        WalletFlow.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for flow in flows:
        member = db.query(Member).filter(Member.id == flow.member_id).first()
        member_name = member.name if member else "未知成员"
        
        result.append({
            "id": flow.id,
            "wallet_id": flow.wallet_id,
            "transaction_id": flow.transaction_id,
            "member_id": flow.member_id,
            "member_name": member_name,
            "flow_type": flow.flow_type,
            "amount": flow.amount,
            "balance_before": flow.balance_before,
            "balance_after": flow.balance_after,
            "created_at": flow.created_at
        })
    
    return result

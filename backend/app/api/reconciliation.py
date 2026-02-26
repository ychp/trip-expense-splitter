from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.wallet_member import WalletMember
from app.models.member import Member
from app.models.wallet import Wallet
from app.models.transaction_split import TransactionSplit
from app.models.transaction import Transaction
from app.schemas.reconciliation import ReconciliationReport, MemberSettlement, WalletReconciliation

router = APIRouter()


@router.get("/wallet/{wallet_id}", response_model=WalletReconciliation)
def get_wallet_reconciliation(
    wallet_id: int,
    db: Session = Depends(get_db)
):
    wallet_members = db.query(WalletMember).filter(WalletMember.wallet_id == wallet_id).all()
    
    if not wallet_members:
        raise HTTPException(status_code=404, detail="钱包没有成员")
    
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="钱包不存在")
    
    total_balance = sum(wm.balance for wm in wallet_members)
    
    member_details = []
    for wm in wallet_members:
        member = db.query(Member).filter(Member.id == wm.member_id).first()
        
        splits = db.query(TransactionSplit).filter(TransactionSplit.member_id == wm.member_id).all()
        split_amount = sum(s.amount for s in splits)
        
        member_details.append({
            "member_id": wm.member_id,
            "member_name": member.name if member else "未知成员",
            "current_balance": wm.balance,
            "total_deposited": wm.balance + split_amount,
            "total_spent": split_amount,
            "share_ratio": round(wm.balance / total_balance * 100, 2) if total_balance > 0 else 0
        })
    
    settlements = calculate_settlements(wallet_members, db)
    
    return {
        "wallet_id": wallet_id,
        "wallet_name": wallet.name,
        "total_balance": sum(wm.balance for wm in wallet_members),
        "member_count": len(wallet_members),
        "members": member_details,
        "settlements": settlements
    }


@router.get("/trip/{trip_id}", response_model=ReconciliationReport)
def get_trip_reconciliation(
    trip_id: int,
    db: Session = Depends(get_db)
):
    wallets = db.query(Wallet).filter(Wallet.trip_id == trip_id).all()
    
    if not wallets:
        raise HTTPException(status_code=404, detail="行程没有钱包")
    
    wallet_reconciliations = []
    all_members = {}
    
    for wallet in wallets:
        wallet_members = db.query(WalletMember).filter(WalletMember.wallet_id == wallet.id).all()
        wallet_total_balance = sum(wm.balance for wm in wallet_members)
        
        member_details = []
        for wm in wallet_members:
            member = db.query(Member).filter(Member.id == wm.member_id).first()
            
            if wm.member_id not in all_members:
                all_members[wm.member_id] = {
                    "member_id": wm.member_id,
                    "member_name": member.name if member else "未知成员",
                    "total_balance": 0,
                    "total_deposited": 0,
                    "total_spent": 0
                }
            
            splits = db.query(TransactionSplit).filter(TransactionSplit.member_id == wm.member_id).all()
            split_amount = sum(s.amount for s in splits)
            
            all_members[wm.member_id]["total_balance"] += wm.balance
            all_members[wm.member_id]["total_deposited"] += wm.balance + split_amount
            all_members[wm.member_id]["total_spent"] += split_amount
            
            member_details.append({
                "member_id": wm.member_id,
                "member_name": member.name if member else "未知成员",
                "current_balance": wm.balance,
                "total_deposited": wm.balance + split_amount,
                "total_spent": split_amount,
                "share_ratio": round(wm.balance / wallet_total_balance * 100, 2) if wallet_total_balance > 0 else 0
            })
        
        wallet_reconciliations.append({
            "wallet_id": wallet.id,
            "wallet_name": wallet.name,
            "total_balance": wallet_total_balance,
            "member_count": len(wallet_members),
            "members": member_details,
            "settlements": calculate_settlements(wallet_members, db)
        })
    
    overall_balance = sum(m["total_balance"] for m in all_members.values())
    
    return {
        "trip_id": trip_id,
        "total_wallets": len(wallets),
        "overall_balance": overall_balance,
        "wallets": wallet_reconciliations,
        "trip_summary": list(all_members.values())
    }


@router.get("/settlements/{wallet_id}", response_model=List[MemberSettlement])
def get_settlements(
    wallet_id: int,
    db: Session = Depends(get_db)
):
    wallet_members = db.query(WalletMember).filter(WalletMember.wallet_id == wallet_id).all()
    
    if not wallet_members:
        return []
    
    return calculate_settlements(wallet_members, db)


def calculate_settlements(wallet_members: List[WalletMember], db: Session) -> List[dict]:
    if not wallet_members:
        return []
    
    total_balance = sum(wm.balance for wm in wallet_members)
    member_count = len(wallet_members)
    
    if total_balance == 0 or member_count < 2:
        return []
    
    avg_balance = total_balance / member_count
    
    debtors = []
    creditors = []
    
    for wm in wallet_members:
        member = db.query(Member).filter(Member.id == wm.member_id).first()
        member_name = member.name if member else "未知成员"
        
        diff = wm.balance - avg_balance
        
        if diff < -0.01:
            debtors.append({
                "member_id": wm.member_id,
                "member_name": member_name,
                "debt_amount": abs(diff)
            })
        elif diff > 0.01:
            creditors.append({
                "member_id": wm.member_id,
                "member_name": member_name,
                "credit_amount": diff
            })
    
    settlements = []
    
    debtors_sorted = sorted(debtors, key=lambda x: x["debt_amount"], reverse=True)
    creditors_sorted = sorted(creditors, key=lambda x: x["credit_amount"], reverse=True)
    
    i = j = 0
    while i < len(debtors_sorted) and j < len(creditors_sorted):
        debtor = debtors_sorted[i]
        creditor = creditors_sorted[j]
        
        amount = min(debtor["debt_amount"], creditor["credit_amount"])
        
        if amount > 0.01:
            settlements.append({
                "from_member_id": debtor["member_id"],
                "from_member_name": debtor["member_name"],
                "to_member_id": creditor["member_id"],
                "to_member_name": creditor["member_name"],
                "amount": round(amount, 2)
            })
        
        debtor["debt_amount"] -= amount
        creditor["credit_amount"] -= amount
        
        if debtor["debt_amount"] < 0.01:
            i += 1
        if creditor["credit_amount"] < 0.01:
            j += 1
    
    return settlements

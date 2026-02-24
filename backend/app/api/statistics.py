from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from app.core.database import get_db
from app.models import Transaction, Category, Account

router = APIRouter()


@router.get("/summary")
def get_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    income = query.filter(Transaction.type == "income").with_entities(
        func.sum(Transaction.amount)
    ).scalar() or 0
    
    expense = query.filter(Transaction.type == "expense").with_entities(
        func.sum(Transaction.amount)
    ).scalar() or 0
    
    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "balance": round(income - expense, 2)
    }


@router.get("/by-category")
def get_by_category(
    type: str = Query(..., description="income 或 expense"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        Category.name,
        func.sum(Transaction.amount).label("total")
    ).join(
        Transaction, Category.id == Transaction.category_id
    ).filter(
        Transaction.type == type
    )
    
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    results = query.group_by(Category.id, Category.name).all()
    
    return [
        {"category": name, "amount": round(total, 2)}
        for name, total in results
    ]


@router.get("/trend")
def get_trend(
    type: str = Query(..., description="income 或 expense"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        func.strftime("%Y-%m", Transaction.transaction_date).label("month"),
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.type == type
    )
    
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    results = query.group_by("month").order_by("month").all()
    
    return [
        {"month": month, "amount": round(total, 2)}
        for month, total in results
    ]


@router.get("/accounts")
def get_accounts_summary(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    
    return [
        {
            "id": acc.id,
            "name": acc.name,
            "type": acc.type,
            "balance": round(acc.balance, 2)
        }
        for acc in accounts
    ]

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.models.category import Category
from app.models.member import Member
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter()


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    trip_id: Optional[int] = Query(None),
    wallet_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if trip_id:
        query = query.filter(Transaction.trip_id == trip_id)
    if wallet_id:
        query = query.filter(Transaction.wallet_id == wallet_id)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    transactions = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()
    
    result = []
    for txn in transactions:
        wallet = db.query(Wallet).filter(Wallet.id == txn.wallet_id).first()
        category = db.query(Category).filter(Category.id == txn.category_id).first()
        payer = db.query(Member).filter(Member.id == txn.payer_id).first()
        
        result.append({
            "id": txn.id,
            "trip_id": txn.trip_id,
            "wallet_id": txn.wallet_id,
            "category_id": txn.category_id,
            "transaction_type": txn.transaction_type,
            "amount": txn.amount,
            "payer_id": txn.payer_id,
            "transaction_date": txn.transaction_date.strftime('%Y-%m-%d'),
            "remark": txn.remark,
            "created_at": txn.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "wallet": {"id": wallet.id, "name": wallet.name} if wallet else None,
            "category": {"id": category.id, "name": category.name} if category else None,
            "payer": {"id": payer.id, "name": payer.name} if payer else None,
            "splits": []
        })
    
    return result


@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    transaction_data = transaction.model_dump()
    transaction_date_str = transaction_data.pop('transaction_date')
    transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d')
    
    db_transaction = Transaction(
        **transaction_data,
        transaction_date=transaction_date
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # 重新查询以获取关联数据
    db_transaction = db.query(Transaction).options(
        joinedload(Transaction.wallet),
        joinedload(Transaction.category),
        joinedload(Transaction.trip)
    ).filter(Transaction.id == db_transaction.id).first()
    
    return db_transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).options(
        joinedload(Transaction.wallet),
        joinedload(Transaction.category),
        joinedload(Transaction.trip)
    ).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="支出明细不存在")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="支出明细不存在")
    
    update_data = transaction.model_dump(exclude_unset=True)
    
    if 'transaction_date' in update_data:
        transaction_date_str = update_data.pop('transaction_date')
        update_data['transaction_date'] = datetime.strptime(transaction_date_str, '%Y-%m-%d')
    
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    
    # 重新查询以获取关联数据
    db_transaction = db.query(Transaction).options(
        joinedload(Transaction.wallet),
        joinedload(Transaction.category),
        joinedload(Transaction.trip)
    ).filter(Transaction.id == db_transaction.id).first()
    
    return db_transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="支出明细不存在")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "支出明细已删除"}

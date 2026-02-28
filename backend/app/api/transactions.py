from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.core.database import get_db
from app.core.logging import get_logger
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.models.category import Category
from app.models.member import Member
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.stats_service import StatsService

router = APIRouter()
logger = get_logger(__name__)


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
    
    if not transactions:
        return []
    
    wallet_ids = list({t.wallet_id for t in transactions})
    category_ids = list({t.category_id for t in transactions if t.category_id})
    payer_ids = list({t.payer_id for t in transactions if t.payer_id})
    
    wallets_map = {w.id: w for w in db.query(Wallet).filter(Wallet.id.in_(wallet_ids)).all()}
    categories_map = {c.id: c for c in db.query(Category).filter(Category.id.in_(category_ids)).all()}
    payers_map = {p.id: p for p in db.query(Member).filter(Member.id.in_(payer_ids)).all()}
    
    result = []
    for txn in transactions:
        wallet = wallets_map.get(txn.wallet_id)
        category = categories_map.get(txn.category_id) if txn.category_id else None
        payer = payers_map.get(txn.payer_id) if txn.payer_id else None
        
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
    
    # 更新统计数据
    try:
        StatsService.update_all_stats(db_transaction.trip_id, db)
    except Exception as e:
        print(f"Warning: Failed to update stats: {e}")
    
    return db_transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
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
    
    # 更新统计数据
    try:
        StatsService.update_all_stats(db_transaction.trip_id, db)
    except Exception as e:
        print(f"Warning: Failed to update stats: {e}")
    
    return db_transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="支出明细不存在")
    
    trip_id = db_transaction.trip_id
    db.delete(db_transaction)
    db.commit()
    
    # 更新统计数据
    try:
        StatsService.update_all_stats(trip_id, db)
    except Exception as e:
        print(f"Warning: Failed to update stats: {e}")
    
    return {"message": "支出明细已删除"}

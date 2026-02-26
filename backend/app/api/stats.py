from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from collections import defaultdict
import time

from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.transaction_split import TransactionSplit
from app.models.wallet import Wallet
from app.models.wallet_member import WalletMember
from app.models.member import Member
from app.models.category import Category

router = APIRouter()

# 简单的内存缓存
_cache = {}
_cache_time = {}
CACHE_TTL = 30  # 缓存30秒

def get_cached(key):
    """获取缓存数据"""
    if key in _cache and time.time() - _cache_time.get(key, 0) < CACHE_TTL:
        return _cache[key]
    return None

def set_cache(key, value):
    """设置缓存数据"""
    _cache[key] = value
    _cache_time[key] = time.time()


@router.get("/per-person/{trip_id}")
def get_per_person_stats(trip_id: int, db: Session = Depends(get_db)):
    """获取人均支出统计 - 缓存优化版本"""
    cache_key = f"stats_per_person_{trip_id}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    # 1. 一次性获取所有成员
    members = db.query(Member).filter(Member.trip_id == trip_id).all()
    if not members:
        raise HTTPException(status_code=404, detail="该行程暂无成员")
    
    member_ids = [m.id for m in members]
    
    # 2. 使用单个复杂查询获取所有需要的数据
    # 这个查询一次性获取：成员总支出、分类支出
    stats_query = db.query(
        TransactionSplit.member_id,
        Category.name.label('category_name'),
        func.sum(TransactionSplit.amount).label('amount')
    ).join(
        Transaction, Transaction.id == TransactionSplit.transaction_id
    ).join(
        Category, Category.id == Transaction.category_id
    ).filter(
        Transaction.trip_id == trip_id,
        TransactionSplit.member_id.in_(member_ids)
    ).group_by(
        TransactionSplit.member_id,
        Category.name
    ).all()
    
    # 3. 构建成员统计结果
    member_stats = {}
    for member in members:
        member_stats[member.id] = {
            "member_id": member.id,
            "member_name": member.name,
            "total_amount": 0.0,
            "by_category": {},
            "by_wallet": {}
        }
    
    # 4. 处理查询结果
    category_totals = defaultdict(float)
    for member_id, category_name, amount in stats_query:
        if member_id in member_stats:
            amount_float = float(amount or 0)
            member_stats[member_id]["by_category"][category_name] = amount_float
            member_stats[member_id]["total_amount"] += amount_float
            category_totals[category_name] += amount_float
    
    # 5. 计算总支出和平均值
    total_expense = sum(stat["total_amount"] for stat in member_stats.values())
    average_expense = total_expense / len(members) if members else 0
    
    # 6. 计算分类占比
    category_ratios = {
        category: round(amount / total_expense * 100, 2) if total_expense > 0 else 0
        for category, amount in category_totals.items()
    }
    
    result = {
        "trip_id": trip_id,
        "total_expense": round(total_expense, 2),
        "average_expense": round(average_expense, 2),
        "member_count": len(members),
        "member_stats": list(member_stats.values()),
        "category_totals": {k: round(v, 2) for k, v in category_totals.items()},
        "category_ratios": category_ratios
    }
    
    # 7. 缓存结果
    set_cache(cache_key, result)
    
    return result


@router.get("/wallet-summary/{trip_id}")
def get_wallet_summary(trip_id: int, db: Session = Depends(get_db)):
    """获取钱包汇总统计 - 缓存优化版本"""
    cache_key = f"stats_wallet_summary_{trip_id}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    # 1. 一次性获取所有钱包
    wallets = db.query(Wallet).filter(Wallet.trip_id == trip_id).all()
    if not wallets:
        return {"trip_id": trip_id, "wallets": []}
    
    wallet_ids = [w.id for w in wallets]
    
    # 2. 使用SQL聚合查询获取每个钱包的统计数据
    wallet_stats = db.query(
        Transaction.wallet_id,
        func.count(Transaction.id).label('transaction_count'),
        func.sum(func.case([(Transaction.transaction_type == 'expense', Transaction.amount)], else_=0)).label('total_spent'),
        func.sum(func.case([(Transaction.transaction_type == 'deposit', Transaction.amount)], else_=0)).label('total_deposited')
    ).filter(
        Transaction.wallet_id.in_(wallet_ids)
    ).group_by(
        Transaction.wallet_id
    ).all()
    
    wallet_stats_map = {
        wallet_id: {
            'transaction_count': count or 0,
            'total_spent': float(spent or 0),
            'total_deposited': float(deposited or 0)
        }
        for wallet_id, count, spent, deposited in wallet_stats
    }
    
    # 3. 一次性获取所有钱包成员余额
    wallet_members_all = db.query(WalletMember).filter(
        WalletMember.wallet_id.in_(wallet_ids)
    ).all()
    
    # 按钱包ID分组
    wallet_members_map = defaultdict(list)
    for wm in wallet_members_all:
        wallet_members_map[wm.wallet_id].append(wm)
    
    # 4. 构建结果
    wallet_summary = []
    for wallet in wallets:
        wallet_members = wallet_members_map.get(wallet.id, [])
        balance_by_member = {wm.member_id: wm.balance for wm in wallet_members}
        total_balance = sum(wm.balance for wm in wallet_members)
        
        stats = wallet_stats_map.get(wallet.id, {
            'transaction_count': 0,
            'total_spent': 0,
            'total_deposited': 0
        })
        
        wallet_summary.append({
            "wallet_id": wallet.id,
            "wallet_name": wallet.name,
            "balance_by_member": balance_by_member,
            "total_balance": round(total_balance, 2),
            "transaction_count": stats['transaction_count'],
            "total_deposited": round(stats['total_deposited'], 2),
            "total_spent": round(stats['total_spent'], 2),
            "remaining": round(total_balance, 2)
        })
    
    result = {
        "trip_id": trip_id,
        "wallets": wallet_summary
    }
    
    # 5. 缓存结果
    set_cache(cache_key, result)
    
    return result

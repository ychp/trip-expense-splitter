from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.database import get_db
from app.models.trip_stats import TripStats
from app.models.member_stats import MemberStats
from app.models.wallet_stats import WalletStats
from app.services.stats_service import StatsService

router = APIRouter()


@router.get("/per-person/{trip_id}")
def get_per_person_stats(trip_id: int, db: Session = Depends(get_db)):
    """获取人均支出统计 - 从统计表读取（高性能版本）"""
    
    # 1. 获取行程级统计
    trip_stats = db.query(TripStats).filter(TripStats.trip_id == trip_id).first()
    if not trip_stats:
        # 如果统计表不存在，则触发计算
        StatsService.update_trip_stats(trip_id, db)
        trip_stats = db.query(TripStats).filter(TripStats.trip_id == trip_id).first()
    
    # 2. 获取成员级统计
    member_stats_list = db.query(MemberStats).filter(
        MemberStats.trip_id == trip_id
    ).all()
    
    if not trip_stats:
        raise HTTPException(status_code=404, detail="该行程暂无统计数据")
    
    # 3. 解析JSON字符串并构建返回结果
    category_totals = json.loads(trip_stats.category_totals) if trip_stats.category_totals else {}
    category_ratios = json.loads(trip_stats.category_ratios) if trip_stats.category_ratios else {}
    
    result = {
        "trip_id": trip_id,
        "total_expense": trip_stats.total_expense,
        "average_expense": trip_stats.average_expense,
        "member_count": trip_stats.member_count,
        "member_stats": [
            {
                "member_id": ms.member_id,
                "member_name": ms.member_name,
                "total_amount": ms.total_amount,
                "by_category": json.loads(ms.by_category) if ms.by_category else {},
                "by_wallet": json.loads(ms.by_wallet) if ms.by_wallet else {}
            }
            for ms in member_stats_list
        ],
        "category_totals": category_totals,
        "category_ratios": category_ratios
    }
    
    return result


@router.get("/wallet-summary/{trip_id}")
def get_wallet_summary(trip_id: int, db: Session = Depends(get_db)):
    """获取钱包汇总统计 - 从统计表读取（高性能版本）"""
    
    # 获取钱包统计
    wallet_stats_list = db.query(WalletStats).filter(
        WalletStats.trip_id == trip_id
    ).all()
    
    if not wallet_stats_list:
        # 如果统计表不存在，则触发计算
        StatsService.update_wallet_stats(trip_id, db)
        wallet_stats_list = db.query(WalletStats).filter(
            WalletStats.trip_id == trip_id
        ).all()
    
    result = {
        "trip_id": trip_id,
        "wallets": [
            {
                "wallet_id": ws.wallet_id,
                "wallet_name": ws.wallet_name,
                "balance_by_member": json.loads(ws.balance_by_member) if ws.balance_by_member else {},
                "total_balance": ws.total_balance,
                "transaction_count": ws.transaction_count,
                "total_deposited": ws.total_deposited,
                "total_spent": ws.total_spent,
                "remaining": ws.remaining
            }
            for ws in wallet_stats_list
        ]
    }
    
    return result


@router.post("/refresh/{trip_id}")
def refresh_stats(trip_id: int, db: Session = Depends(get_db)):
    """手动刷新统计数据 - 管理员接口"""
    try:
        StatsService.update_all_stats(trip_id, db)
        return {"message": "统计数据已刷新", "trip_id": trip_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刷新失败: {str(e)}")


@router.get("/info/{trip_id}")
def get_stats_info(trip_id: int, db: Session = Depends(get_db)):
    """获取统计表元信息（用于调试）"""
    trip_stats = db.query(TripStats).filter(TripStats.trip_id == trip_id).first()
    member_stats_count = db.query(MemberStats).filter(MemberStats.trip_id == trip_id).count()
    wallet_stats_count = db.query(WalletStats).filter(WalletStats.trip_id == trip_id).count()
    
    if not trip_stats:
        return {
            "trip_id": trip_id,
            "has_stats": False,
            "message": "统计数据未生成，请先创建交易或手动刷新"
        }
    
    return {
        "trip_id": trip_id,
        "has_stats": True,
        "trip_stats_updated_at": trip_stats.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "member_stats_count": member_stats_count,
        "wallet_stats_count": wallet_stats_count,
        "transaction_count": trip_stats.transaction_count
    }

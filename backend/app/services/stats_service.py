from sqlalchemy.orm import Session
from sqlalchemy import func, case
from collections import defaultdict
from typing import List
import json

from app.models.trip_stats import TripStats
from app.models.member_stats import MemberStats
from app.models.wallet_stats import WalletStats
from app.models.member import Member
from app.models.transaction import Transaction
from app.models.transaction_split import TransactionSplit
from app.models.wallet import Wallet
from app.models.wallet_member import WalletMember
from app.models.category import Category


class StatsService:
    """统计数据服务 - 负责维护统计表数据"""
    
    @staticmethod
    def update_trip_stats(trip_id: int, db: Session):
        """更新行程统计数据"""
        try:
            # 获取所有成员
            members = db.query(Member).filter(Member.trip_id == trip_id).all()
            if not members:
                return
            
            member_ids = [m.id for m in members]
            
            # 获取分类统计
            category_stats = db.query(
                Category.name,
                func.sum(TransactionSplit.amount).label('amount')
            ).join(
                Transaction, Transaction.id == TransactionSplit.transaction_id
            ).join(
                Category, Category.id == Transaction.category_id
            ).filter(
                Transaction.trip_id == trip_id
            ).group_by(Category.name).all()
            
            # 计算总支出
            total_expense = float(sum(amount for _, amount in category_stats))
            average_expense = total_expense / len(members) if members else 0
            
            # 构建分类数据
            category_totals = {name: float(amount) for name, amount in category_stats}
            category_ratios = {
                name: round(amount / total_expense * 100, 2) if total_expense > 0 else 0
                for name, amount in category_totals.items()
            }
            
            # 获取交易总数
            transaction_count = db.query(func.count(Transaction.id)).filter(
                Transaction.trip_id == trip_id
            ).scalar()
            
            # 更新或创建统计记录
            stats = db.query(TripStats).filter(TripStats.trip_id == trip_id).first()
            if not stats:
                stats = TripStats(trip_id=trip_id)
                db.add(stats)
            
            stats.total_expense = total_expense
            stats.average_expense = average_expense
            stats.member_count = len(members)
            stats.category_totals = json.dumps(category_totals, ensure_ascii=False)
            stats.category_ratios = json.dumps(category_ratios, ensure_ascii=False)
            stats.transaction_count = transaction_count or 0
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def update_member_stats(trip_id: int, db: Session):
        """更新成员统计数据"""
        try:
            members = db.query(Member).filter(Member.trip_id == trip_id).all()
            if not members:
                return
            
            member_ids = [m.id for m in members]
            
            # 获取每个成员的总支出和分类支出
            member_category_stats = db.query(
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
            
            # 整理数据
            member_data = defaultdict(lambda: {'by_category': defaultdict(float), 'total': 0.0})
            for member_id, category, amount in member_category_stats:
                amount_float = float(amount)
                member_data[member_id]['by_category'][category] = amount_float
                member_data[member_id]['total'] += amount_float
            
            # 计算平均值
            total_expense = sum(data['total'] for data in member_data.values())
            average_expense = total_expense / len(members) if members else 0
            
            # 更新或创建每个成员的统计
            for member in members:
                data = member_data.get(member.id, {'by_category': {}, 'total': 0.0})
                
                stats = db.query(MemberStats).filter(
                    MemberStats.trip_id == trip_id,
                    MemberStats.member_id == member.id
                ).first()
                
                if not stats:
                    stats = MemberStats(trip_id=trip_id, member_id=member.id)
                    db.add(stats)
                
                stats.member_name = member.name
                stats.total_amount = data['total']
                stats.by_category = json.dumps(dict(data['by_category']), ensure_ascii=False)
                stats.by_wallet = json.dumps({}, ensure_ascii=False)
                stats.should_pay = average_expense
                stats.balance = data['total'] - average_expense
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def update_wallet_stats(trip_id: int, db: Session):
        """更新钱包统计数据"""
        try:
            wallets = db.query(Wallet).filter(Wallet.trip_id == trip_id).all()
            if not wallets:
                return
            
            wallet_ids = [w.id for w in wallets]
            
            # 获取钱包交易统计
            wallet_stats_data = db.query(
                Transaction.wallet_id,
                func.count(Transaction.id).label('transaction_count'),
                func.sum(case((Transaction.transaction_type == 'expense', Transaction.amount), else_=0)).label('total_spent'),
                func.sum(case((Transaction.transaction_type == 'deposit', Transaction.amount), else_=0)).label('total_deposited')
            ).filter(
                Transaction.wallet_id.in_(wallet_ids)
            ).group_by(Transaction.wallet_id).all()
            
            wallet_stats_map = {}
            for wallet_id, count, spent, deposited in wallet_stats_data:
                wallet_stats_map[wallet_id] = {
                    'transaction_count': count or 0,
                    'total_spent': float(spent or 0),
                    'total_deposited': float(deposited or 0)
                }
            
            # 更新或创建每个钱包的统计
            for wallet in wallets:
                stats = wallet_stats_map.get(wallet.id, {
                    'transaction_count': 0,
                    'total_spent': 0.0,
                    'total_deposited': 0.0
                })
                
                # 获取成员余额
                wallet_members = db.query(WalletMember).filter(
                    WalletMember.wallet_id == wallet.id
                ).all()
                
                balance_by_member = {wm.member_id: wm.balance for wm in wallet_members}
                total_balance = sum(wm.balance for wm in wallet_members)
                
                wallet_stat = db.query(WalletStats).filter(
                    WalletStats.wallet_id == wallet.id
                ).first()
                
                if not wallet_stat:
                    wallet_stat = WalletStats(trip_id=trip_id, wallet_id=wallet.id)
                    db.add(wallet_stat)
                
                wallet_stat.wallet_name = wallet.name
                wallet_stat.balance_by_member = json.dumps(balance_by_member, ensure_ascii=False)
                wallet_stat.total_balance = total_balance
                wallet_stat.transaction_count = stats['transaction_count']
                wallet_stat.total_deposited = stats['total_deposited']
                wallet_stat.total_spent = stats['total_spent']
                wallet_stat.remaining = total_balance
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def update_all_stats(trip_id: int, db: Session):
        """更新所有统计数据（事务变更时调用）"""
        try:
            StatsService.update_trip_stats(trip_id, db)
            StatsService.update_member_stats(trip_id, db)
            StatsService.update_wallet_stats(trip_id, db)
        except Exception as e:
            raise e

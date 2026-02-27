from sqlalchemy import Column, Integer, Float, DateTime, Text, Index
from datetime import datetime
from app.core.database import Base


class WalletStats(Base):
    __tablename__ = "wallet_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False, comment="行程ID")
    wallet_id = Column(Integer, nullable=False, unique=True, comment="钱包ID")
    wallet_name = Column(Integer, comment="钱包名称冗余字段")
    
    balance_by_member = Column(Text, comment="成员余额JSON字符串")
    total_balance = Column(Float, default=0.0, comment="总余额")
    
    transaction_count = Column(Integer, default=0, comment="交易数量")
    total_deposited = Column(Float, default=0.0, comment="总存入")
    total_spent = Column(Float, default=0.0, comment="总支出")
    remaining = Column(Float, default=0.0, comment="剩余金额")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (
        Index("ix_wallet_stats_trip_id", "trip_id"),
        Index("ix_wallet_stats_wallet_id", "wallet_id"),
        Index("ix_wallet_stats_updated_at", "updated_at"),
    )

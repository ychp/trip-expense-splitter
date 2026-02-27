from sqlalchemy import Column, Integer, Float, DateTime, Text, Index
from datetime import datetime
from app.core.database import Base


class MemberStats(Base):
    __tablename__ = "member_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False, comment="行程ID")
    member_id = Column(Integer, nullable=False, comment="成员ID")
    member_name = Column(Integer, comment="成员名称冗余字段")
    
    total_amount = Column(Float, default=0.0, comment="总支出")
    by_category = Column(Text, comment="按分类统计JSON字符串")
    by_wallet = Column(Text, comment="按钱包统计JSON字符串")
    
    should_pay = Column(Float, default=0.0, comment="应付金额（平均值）")
    actual_paid = Column(Float, default=0.0, comment="实际支付金额")
    balance = Column(Float, default=0.0, comment="差额（实际-应付）")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (
        Index("ix_member_stats_trip_id", "trip_id"),
        Index("ix_member_stats_member_id", "member_id"),
        Index("ix_member_stats_trip_member", "trip_id", "member_id", unique=True),
    )

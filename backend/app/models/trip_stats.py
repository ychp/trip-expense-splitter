from sqlalchemy import Column, Integer, Float, DateTime, Text, Index
from datetime import datetime
from app.core.database import Base


class TripStats(Base):
    __tablename__ = "trip_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False, unique=True, comment="行程ID")
    total_expense = Column(Float, default=0.0, comment="总支出")
    average_expense = Column(Float, default=0.0, comment="人均支出")
    member_count = Column(Integer, default=0, comment="成员数量")
    category_totals = Column(Text, comment="分类汇总JSON字符串")
    category_ratios = Column(Text, comment="分类占比JSON字符串")
    transaction_count = Column(Integer, default=0, comment="交易总数")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (
        Index("ix_trip_stats_trip_id", "trip_id"),
        Index("ix_trip_stats_updated_at", "updated_at"),
    )

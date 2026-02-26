from sqlalchemy import Column, Integer, Float, String, DateTime, Index
from datetime import datetime

from app.core.database import Base


class TransactionSplit(Base):
    __tablename__ = "transaction_splits"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, nullable=False, index=True)
    member_id = Column(Integer, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    split_method = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # 复合索引优化查询
    __table_args__ = (
        Index('idx_transaction_member', 'transaction_id', 'member_id'),
    )

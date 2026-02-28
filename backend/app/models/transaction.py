from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from datetime import datetime

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index('idx_trip_wallet', 'trip_id', 'wallet_id'),
        Index('idx_transaction_date', 'transaction_date'),
        Index('idx_trip_date', 'trip_id', 'transaction_date'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False, index=True)
    wallet_id = Column(Integer, nullable=False, index=True)
    category_id = Column(Integer, nullable=True, index=True)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    payer_id = Column(Integer, nullable=True, index=True)
    transaction_date = Column(DateTime, nullable=False)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False)
    wallet_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=True)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    payer_id = Column(Integer, nullable=True)
    transaction_date = Column(DateTime, nullable=False)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

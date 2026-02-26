from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from app.core.database import Base


class WalletFlow(Base):
    __tablename__ = "wallet_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, nullable=False)
    transaction_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    flow_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    balance_before = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

from sqlalchemy import Column, Integer, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class WalletMember(Base):
    __tablename__ = "wallet_members"
    __table_args__ = (
        UniqueConstraint('wallet_id', 'member_id', name='unique_wallet_member'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    balance = Column(Float, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

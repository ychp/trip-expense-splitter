from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.database import Base


class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    trip_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    type = Column(String(20), nullable=False)
    sort_order = Column(Integer, default=0)

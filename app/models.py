from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    price = Column(Float)
    author = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
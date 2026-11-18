from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, Boolean, Numeric
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="player") 
    created_at = Column(DateTime, default=datetime.utcnow)
    is_online = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

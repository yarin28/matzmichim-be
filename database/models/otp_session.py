
from enum import unique
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from database.models.base import Base

class OTP_Session(Base):
    __tablename__ = 'otp_session'
    otp = Column(String(6),primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_end = Column(DateTime, nullable=False)
    
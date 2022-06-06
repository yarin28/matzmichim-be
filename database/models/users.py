from sqlalchemy import Column,Integer,String
from database.models.base import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(String(250), primary_key=True)
    email = Column(String(250), nullable=False)
    full_name = Column(String(250), nullable=False)
    phone = Column(String(15), nullable=False)
    

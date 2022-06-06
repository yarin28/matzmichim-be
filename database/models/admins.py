
from sqlalchemy import INTEGER, Column, Identity,Integer,String
from database.models.base import Base

class admins(Base):
    __tablename__ = 'admins'
    # __table_args__ = {'sqlite_autoincrement': True}
    username = Column(String(250),primary_key=True, nullable=False)
    password = Column(String(250), nullable=False)
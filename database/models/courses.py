from sqlalchemy import Integer, Column, Identity,Integer,String
from database.models.base import Base

class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)

    


    
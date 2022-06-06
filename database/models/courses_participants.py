from sqlalchemy import Integer, Column, Identity,Integer,String, ForeignKey
from database.models.base import Base

class CoursesParticipants(Base):
    __tablename__ = 'courses_participants'
    course_id = Column(Integer, ForeignKey("courses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    


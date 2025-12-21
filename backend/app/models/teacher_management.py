from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base

class TeacherManagement(Base):
    __tablename__ = "teacher_management"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
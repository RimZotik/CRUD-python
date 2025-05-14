from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE')),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'))
)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    courses = relationship('Course', secondary=student_course, backref='students')
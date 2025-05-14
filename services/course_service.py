from sqlalchemy.orm import joinedload
from models.course import Course
from db import SessionLocal

def add_course(name, duration, teacher_id):
    with SessionLocal() as session:
        course = Course(name=name, duration=duration, teacher_id=teacher_id)
        session.add(course)
        session.commit()

def get_all_courses():
    with SessionLocal() as session:
        return session.query(Course).options(joinedload(Course.teacher)).all()

def get_course(course_id):
    with SessionLocal() as session:
        return session.get(Course, course_id)

def update_course(course_id, name, duration, teacher_id):
    with SessionLocal() as session:
        course = session.get(Course, course_id)
        if course:
            course.name = name
            course.duration = duration
            course.teacher_id = teacher_id
            session.commit()

def delete_course(session, course_id):
    course = session.get(Course, course_id)
    if course:
        session.delete(course)
        session.commit()
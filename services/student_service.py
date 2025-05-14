from sqlalchemy.orm import joinedload
from models.student import Student
from models.course import Course
from db import SessionLocal

def add_student(name, age, course_ids):
    with SessionLocal() as session:
        student = Student(name=name, age=age)
        student.courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
        session.add(student)
        session.commit()

def get_all_students():
    with SessionLocal() as session:
        return session.query(Student).all()

def get_student(student_id):
    with SessionLocal() as session:
        return session.query(Student).options(joinedload(Student.courses)).get(student_id)

def update_student(student_id, name, age, course_ids):
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if student:
            student.name = name
            student.age = age
            student.courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
            session.commit()

def update_student_courses(student_id, course_ids):
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if student:
            student.courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
            session.commit()

def delete_student(student_id):
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if student:
            session.delete(student)
            session.commit()
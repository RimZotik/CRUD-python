from models.teacher import Teacher
from db import SessionLocal

def add_teacher(name, age):
    with SessionLocal() as session:
        teacher = Teacher(name=name, age=age)
        session.add(teacher)
        session.commit()

def get_all_teachers():
    with SessionLocal() as session:
        return session.query(Teacher).all()

def get_teacher(teacher_id):
    with SessionLocal() as session:
        return session.get(Teacher, teacher_id)

def update_teacher(teacher_id, name, age):
    with SessionLocal() as session:
        teacher = session.get(Teacher, teacher_id)
        if teacher:
            teacher.name = name
            teacher.age = age
            session.commit()

def delete_teacher(teacher_id):
    with SessionLocal() as session:
        teacher = session.get(Teacher, teacher_id)
        if teacher:
            session.delete(teacher)
            session.commit()
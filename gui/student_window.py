import tkinter as tk
from tkinter import messagebox
from services.course_service import get_all_courses
from services.student_service import add_student, get_student, update_student

def open_student_window(student_id=None):
    win = tk.Toplevel()
    win.title("Редактировать ученика" if student_id else "Добавить ученика")

    tk.Label(win, text="Имя").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Возраст").pack()
    age_entry = tk.Entry(win)
    age_entry.pack()

    tk.Label(win, text="Выберите курсы").pack()
    course_vars = []
    courses = get_all_courses()
    selected_ids = []

    if student_id:
        student = get_student(student_id)
        if student:
            name_entry.insert(0, student.name)
            age_entry.insert(0, str(student.age))
            selected_ids = [c.id for c in student.courses]

    for course in courses:
        var = tk.IntVar(value=1 if course.id in selected_ids else 0)
        chk = tk.Checkbutton(win, text=course.name, variable=var)
        chk.pack()
        course_vars.append((var, course.id))

    def save():
        name = name_entry.get().strip()
        age_text = age_entry.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст должен быть положительным числом.")
            return

        selected = [cid for var, cid in course_vars if var.get()]
        # Проверка на обязательность хотябы одного курса
        # if not selected:
        #     messagebox.showerror("Ошибка", "Нужно выбрать хотя бы один курс.")
        #     return

        if student_id:
            update_student(student_id, name, age, selected)
        else:
            add_student(name, age, selected)
        win.destroy()

    tk.Button(win, text="Сохранить", command=save).pack()

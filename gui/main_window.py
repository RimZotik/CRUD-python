import tkinter as tk
from tkinter import ttk, messagebox
from gui.teacher_window import open_teacher_window
from gui.course_window import open_course_window
from gui.student_window import open_student_window
from services.teacher_service import get_all_teachers, delete_teacher
from services.course_service import get_all_courses, delete_course
from services.student_service import get_all_students, delete_student
from models.student import student_course
import models
from db import SessionLocal

current_table = None

def create_main_window():
    root = tk.Tk()
    root.title("Учебная система")

    global current_table

    add_frame = tk.Frame(root)
    add_frame.pack(fill=tk.X, padx=10, pady=5)

    tk.Button(add_frame, text="Добавить учителя", command=open_teacher_window).pack(side=tk.LEFT, padx=5)
    tk.Button(add_frame, text="Создать курс", command=open_course_window).pack(side=tk.LEFT, padx=5)
    tk.Button(add_frame, text="Создать ученика", command=open_student_window).pack(side=tk.LEFT, padx=5)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите строку для удаления")
            return

        item = tree.item(selected[0])
        values = item["values"]
        record_id = values[0]

        with SessionLocal() as session:
            try:
                if current_table == "teacher":
                    delete_teacher(session, record_id)
                elif current_table == "course":
                    delete_course(session, record_id)
                elif current_table == "student":
                    delete_student(session, record_id)
                elif current_table == "student_course":
                    student_id = values[0]
                    course_id = values[2]

                    session.execute(
                        student_course.delete().where(
                            (student_course.c.student_id == student_id) &
                            (student_course.c.course_id == course_id)
                        )
                    )
                    session.commit()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка при удалении", str(e))
                return

        tree.delete(selected[0])

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Изменение", "Выберите строку для изменения")
            return

        item = tree.item(selected[0])
        record_id = int(item["values"][0])

        if current_table == "teacher":
            open_teacher_window(record_id)
        elif current_table == "course":
            open_course_window(record_id)
        elif current_table == "student":
            open_student_window(record_id)
        else:
            messagebox.showinfo("Изменение", "Нельзя редактировать эту таблицу.")

    tk.Button(add_frame, text="Изменить", command=edit_selected).pack(side=tk.LEFT, padx=5)
    tk.Button(add_frame, text="Удалить", command=delete_selected).pack(side=tk.LEFT, padx=5)

    # Таблица
    tree = ttk.Treeview(root, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def configure_tree_columns(column_names):
        tree["columns"] = column_names
        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

    def load_teachers():
        global current_table
        current_table = "teacher"
        tree.delete(*tree.get_children())
        columns = models.teacher.Teacher.__table__.columns.keys()
        configure_tree_columns(columns)
        for t in get_all_teachers():
            tree.insert("", "end", values=[getattr(t, col) for col in columns])

    def load_courses():
        global current_table
        current_table = "course"
        tree.delete(*tree.get_children())

        columns = ["id", "name", "duration", "teacher_name"]
        configure_tree_columns(columns)

        for c in get_all_courses():
            teacher_name = c.teacher.name if c.teacher else "—"
            tree.insert("", "end", values=(c.id, c.name, c.duration, teacher_name))

    def load_students():
        global current_table
        current_table = "student"
        tree.delete(*tree.get_children())
        columns = models.student.Student.__table__.columns.keys()
        configure_tree_columns(columns)
        for s in get_all_students():
            tree.insert("", "end", values=[getattr(s, col) for col in columns])

    def load_student_courses():
        global current_table
        current_table = "student_course"
        tree.delete(*tree.get_children())
        columns = ["student_id", "student_name", "course_id", "course_name"]
        configure_tree_columns(columns)

        with SessionLocal() as session:
            result = session.execute(student_course.select()).fetchall()
            for row in result:
                student = session.get(models.student.Student, row.student_id)
                course = session.get(models.course.Course, row.course_id)
                tree.insert(
                    "", "end",
                    values=(
                        student.id,
                        student.name,
                        course.id,
                        course.name
                    )
                )

    view_frame = tk.Frame(root)
    view_frame.pack(fill=tk.X, padx=10, pady=5)

    tk.Button(view_frame, text="Показать учителей", command=load_teachers).pack(side=tk.LEFT, padx=5)
    tk.Button(view_frame, text="Показать курсы", command=load_courses).pack(side=tk.LEFT, padx=5)
    tk.Button(view_frame, text="Показать учеников", command=load_students).pack(side=tk.LEFT, padx=5)
    tk.Button(view_frame, text="Показать связи Студент-Курс", command=load_student_courses).pack(side=tk.LEFT, padx=5)

    root.mainloop()

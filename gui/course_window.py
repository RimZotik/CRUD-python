import tkinter as tk
from tkinter import messagebox
from services.teacher_service import get_all_teachers
from services.course_service import add_course, get_course, update_course

def open_course_window(course_id=None):
    win = tk.Toplevel()
    win.title("Редактировать курс" if course_id else "Создать курс")

    tk.Label(win, text="Название курса").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Длительность (в часах)").pack()
    duration_entry = tk.Entry(win)
    duration_entry.pack()

    tk.Label(win, text="Выберите учителя").pack()
    teachers = get_all_teachers()
    teacher_var = tk.StringVar(win)
    teacher_names = [t.name for t in teachers]
    teacher_dropdown = tk.OptionMenu(win, teacher_var, *teacher_names)
    teacher_dropdown.pack()

    if course_id:
        course = get_course(course_id)
        if course:
            name_entry.insert(0, course.name)
            duration_entry.insert(0, str(course.duration))
            teacher_var.set(course.teacher.name)

    def save():
        name = name_entry.get().strip()
        duration_text = duration_entry.get().strip()
        teacher_name = teacher_var.get()

        if not name:
            messagebox.showerror("Ошибка", "Название курса не может быть пустым.")
            return

        try:
            duration = int(duration_text)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        selected_teacher = next((t for t in teachers if t.name == teacher_name), None)
        if not selected_teacher:
            messagebox.showerror("Ошибка", "Выберите учителя.")
            return

        if course_id:
            update_course(course_id, name, duration, selected_teacher.id)
        else:
            add_course(name, duration, selected_teacher.id)

        win.destroy()

    tk.Button(win, text="Сохранить", command=save).pack(pady=10)

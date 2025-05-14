import tkinter as tk
from tkinter import messagebox
from services.teacher_service import add_teacher, get_teacher, update_teacher

def open_teacher_window(teacher_id=None):
    win = tk.Toplevel()
    win.title("Редактировать учителя" if teacher_id else "Добавить учителя")

    tk.Label(win, text="Имя").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Возраст").pack()
    age_entry = tk.Entry(win)
    age_entry.pack()

    if teacher_id:
        teacher = get_teacher(teacher_id)
        if teacher:
            name_entry.insert(0, teacher.name)
            age_entry.insert(0, str(teacher.age))

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

        if teacher_id:
            update_teacher(teacher_id, name, age)
        else:
            add_teacher(name, age)

        win.destroy()

    tk.Button(win, text="Сохранить", command=save).pack()

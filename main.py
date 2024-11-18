import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user():
    def register():
        login = login_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not login or not password or not confirm_password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
            conn.commit()
            messagebox.showinfo("Успешно", "Регистрация прошла успешно!")
            register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
        finally:
            conn.close()

    register_window = tk.Toplevel(root)
    register_window.title("Регистрация")

    login_label = tk.Label(register_window, text="Логин:")
    login_label.grid(row=0, column=0, padx=5, pady=5)
    login_entry = tk.Entry(register_window)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(register_window, text="Пароль:")
    password_label.grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    confirm_password_label = tk.Label(register_window, text="Подтверждение пароля:")
    confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
    confirm_password_entry = tk.Entry(register_window, show="*")
    confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

    register_button = tk.Button(register_window, text="Зарегистрироваться", command=register)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)


def authorize():
    login = login_entry.get()
    password = password_entry.get()

    if not login or not password:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Успешно", "Авторизация прошла успешно!")

    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")


create_db()

root = tk.Tk()
root.title("Авторизация")

login_label = tk.Label(root, text="Логин:")
login_label.grid(row=0, column=0, padx=5, pady=5)
login_entry = tk.Entry(root)
login_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(root, text="Пароль:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

authorize_button = tk.Button(root, text="Авторизоваться", command=authorize)
authorize_button.grid(row=2, column=0, columnspan=2, pady=10)

register_button = tk.Button(root, text="Регистрация", command=register_user)
register_button.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
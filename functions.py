import sqlite3, bcrypt, os
from tkinter import *
from tkinter import ttk, messagebox
from sqlite3 import Error

def create_db(db_name, user='admin', pswd='admin@123'):
    try:
        conn =  sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )''')
        cur.execute('INSERT INTO users(username, password) VALUES(?,?)', (user, bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())))
        conn.commit()
        conn.close()
    except Error as e:
        if conn:
            conn.close()
        os.remove(db_name)
        messagebox.showerror("Something went wrong!", e)

def put_entry(entry, placeholder):
    if len(entry.get()) == 0:
        entry.insert(0, placeholder)

def clear_entry(entry):
    entry.delete(0, END)

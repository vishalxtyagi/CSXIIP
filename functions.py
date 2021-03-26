import sqlite3, bcrypt, os, pickle
from tkinter import *
from tkinter import ttk, messagebox
from dotenv import load_dotenv
load_dotenv()

def createDb(user='admin', pswd='admin@123'):
    try:
        conn = sqlite3.connect(os.getenv("DB")) 
        cur = conn.cursor()
        dump_file = open("database/dump.sqlite", "r")
        cur.execute(dump_file.read())
        dump_file.close()
        cur.execute('INSERT INTO users(username, password) VALUES(?,?)', (user, bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())))
        conn.commit()
        conn.close()
    except Exception as e:
        if conn:
            conn.close()
        os.remove(os.getenv("DB"))
        messagebox.showerror("Something went wrong!", e)

def isUserValidate(user, pswd):
    isValidate = False
    conn = sqlite3.connect(os.getenv("DB"))  
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?",(user,))
    for data in cur.fetchall():
        if bcrypt.checkpw(pswd.encode(), data[0]):
            isValidate = True
            break
    else:
        conn.close()
    return isValidate

def createAuth(user):
    auth_file = open("database/auth", "wb")
    pickle.dump(user,auth_file)
    auth_file.close()

def checkAuth():
    isLogged = False
    try:
        conn = sqlite3.connect(os.getenv("DB")) 
        cur = conn.cursor()
        authFile = open("database/auth", "rb")
        cur.execute("SELECT * FROM users WHERE username = ?", (pickle.load(authFile),))
        authFile.close()
        result = cur.fetchone()
        if result is None:
            os.remove("database/auth")
        else:
            isLogged = True
    except Exception as e:
        print(e)
    return isLogged

import sqlite3, bcrypt, os, pickle
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from dotenv import load_dotenv
load_dotenv()

def initDb(user='admin', pswd='admin@123'):
    try:
        if os.path.isfile(os.getenv("DB")) and os.path.getsize(os.getenv("DB")) > 100:
            pass
        else:
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
    initDb()
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
    initDb()
    isLogged = False
    try:
        conn = sqlite3.connect(os.getenv("DB")) 
        cur = conn.cursor()
        authFile = open("database/auth", "rb")
        cur.execute("SELECT * FROM users WHERE username = ?", (pickle.load(authFile),))
        authFile.close()
        result = cur.fetchone()
        conn.close()
        if result is None:
            os.remove("database/auth")
        else:
            isLogged = True
    except Exception as e:
        if conn:
            conn.close()
        print(e)

    return isLogged

def winTitle(title):
    return title + ' | ' + os.getenv("APP_TITLE")

def getTablesFromDB(db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        result = [table[0] for table in cur.fetchall()]
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return []

def getColumnsFromDB(table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + table)
        result = [description[0] for description in cur.description]
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return []

def fetchDataFromTable(column, table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute("SELECT " + column + " FROM " + table)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return []

def execSQL(sql, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute(sql)
        return cur
        conn.close()
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return None

def getDataTypeFromTable(table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute("PRAGMA table_info("+ table +")")
        result = {}
        for x in cur.fetchall():
            result[x[1]] = x[2]
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return {}

def add():
    pass

def delete():
    pass

def update():
    pass

def start(window):
    root = ThemedTk(background=True, theme="breeze")
    app = window(root)
    root.mainloop()
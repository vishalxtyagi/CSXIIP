import sqlite3, bcrypt, os, pickle
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from dotenv import load_dotenv
from main import *
load_dotenv()

def hashpw(pswd):
    result = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())
    return result.decode()

def initDb(user='admin', pswd='admin@123'):
    try:
        if os.path.isfile(os.getenv("DB")) and os.path.getsize(os.getenv("DB")) > 100:
            pass
        else:
            conn = sqlite3.connect(os.getenv("DB")) 
            cur = conn.cursor()
            dump_file = open("database/dump.sqlite", "r")
            cur.executescript(dump_file.read())
            dump_file.close()
            cur.execute('INSERT INTO users(username, password) VALUES("{}","{}")'.format(user, hashpw(pswd)))
            conn.commit()
            conn.close()
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        os.remove(os.getenv("DB"))

def isUserValidate(user, pswd):
    initDb()
    isValidate = False
    try:
        conn = sqlite3.connect(os.getenv("DB"))  
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = '{}'".format(user, hashpw(pswd)))
        result = cur.fetchall()
        conn.close()
    except Exception as e:
        print(e)
        result = []

    pswd = pswd.encode()
    for data in result:
        if bcrypt.checkpw(pswd, data[0].encode()):
            isValidate = True
            break
    return isValidate

def createAuth(user):
    auth_file = open("database/auth", "wb")
    pickle.dump(user,auth_file)
    auth_file.close()

def currentUser():
    try:
        authFile = open("database/auth", "rb")
        user = pickle.load(authFile)
        authFile.close()
        return user
    except:
        return 'guest'

def checkAuth():
    initDb()
    isLogged = False
    try:
        conn = sqlite3.connect(os.getenv("DB")) 
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = '{}'".format(currentUser()))
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
    return '{} | {}'.format(title, os.getenv("APP_TITLE"))

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

def getMenuItems(db=os.getenv("DB")):
    tbl_list = getTablesFromDB()
    tbl_list.remove('sqlite_sequence')
    tbl_list.insert(0, 'dashboard')
    return tbl_list

def getColumnsFromTable(table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(table))
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
        sql = "SELECT {} FROM {}".format(column, table)
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        error(e)
        return []

def addDataToTable(dict_items, table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        sql = 'INSERT INTO {}({}) VALUES({})'.format(table, ', '.join(i for i in dict_items), ', '.join('"{}"'.format(dict_items[i]) for i in dict_items))
        cur.execute(sql)
        conn.commit()
        conn.close()
        success("Record added successfully!")
    except Exception as e:
        if conn:
            conn.close()
        error(e)

def updateDataToTable(dict_items, item_id, table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'UPDATE {} SET {} WHERE id={}'.format(table, ', '.join('{}="{}"'.format(i,j) for i,j in dict_items.items()), item_id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        success("Record updated successfully!")
    except Exception as e:
        if conn:
            conn.close()
        error(e)

def deleteDataFromTable(item_id, table, db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        sql = "DELETE FROM {} WHERE id = {}".format(table, item_id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        success("Record deleted successfully!")
    except Exception as e:
        if conn:
            conn.close()
        error(e)

def fetchRecordFromTable(item_id, table, column="*", db=os.getenv("DB")):
    initDb()
    try:
        conn = sqlite3.connect(db)  
        cur = conn.cursor()
        sql = "SELECT {} FROM {} WHERE id = {}".format(column, table, item_id)
        cur.execute(sql)
        result = cur.fetchone()
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.close()
        print(e)
        return ()

def error(e):
    messagebox.showerror("Something went wrong!", e)

def success(e):
    messagebox.showinfo("Success!", e)

def start(window):
    try:
        root = ThemedTk(background=True, theme="breeze")
        app = window(root)
        root.mainloop()
    except Exception as e:
        print(e)

def startMain():
    try:
        app = MainApp()
        app.mainloop()
    except Exception as e:
        print(e)
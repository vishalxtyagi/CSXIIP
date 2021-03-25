from functions import *
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from ttkthemes import ThemedTk
import sqlite3, bcrypt

class Login():

    def __init__(self,master):
        self.master=master
        self.master.title('Login | School Management System')
        self.master.iconbitmap('images/icon.ico')
        self.master.geometry('450x650')
        self.master.resizable(False, False)
        
        self.username = StringVar()
        self.password = StringVar()

        self.icon = ImageTk.PhotoImage(Image.open('images/icon.ico'))
        lbl_logo = ttk.Label(self.master, image=self.icon)
        content = ttk.Frame(self.master)

        lbl_title = ttk.Label(content, text='School Management System', font=("Segoe UI", 18, "bold")).pack()
        lbl_subtitle = ttk.Label(content, text='Authenticate yourself to continue...', font=("Segoe UI", 14)).pack(pady=(0,20))
        txt_username = ttk.Entry(content, textvariable=self.username)
        txt_password = ttk.Entry(content, textvariable=self.password)
        btn_submit = ttk.Button(content, text="Submit", command=self.validate_user)

        lbl_logo.pack(side=TOP, pady=20)
        content.pack(side=BOTTOM, pady=50)
        txt_username.pack(fill=X)
        txt_password.pack(fill=X)
        btn_submit.pack(fill=X, pady=20)
        
        txt_username.insert(0, "username or email address")
        txt_username.bind("<FocusIn>", lambda args: clear_entry(txt_username))
        txt_username.bind("<FocusOut>", lambda args: put_entry(txt_username, "Please type your username"))

        txt_password.insert(0, "password")
        txt_password.bind("<FocusIn>", lambda args: clear_entry(txt_password))
        txt_password.bind("<FocusOut>", lambda args: put_entry(txt_password, "Please type your password"))

    def validate_user(self, db='school.db'):
        if os.path.isfile(db):
            conn = sqlite3.connect(db)  
            cur = conn.cursor()
            cur.execute("SELECT username, password from users")
            for data in cur.fetchall():
                if data[0] == self.username.get() and bcrypt.checkpw(self.password.get().encode(), data[1]):
                    self.master.destroy() 
                else:
                    messagebox.showerror("Error","Please Make Sure That the Details are Correct")
        else:
            create_db(db)
            login.validate_user()

if __name__ == '__main__':
    root = ThemedTk(background=True, theme="breeze")
    login = Login(root)
    root.mainloop()
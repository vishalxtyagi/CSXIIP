import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image as pilImage
from dotenv import load_dotenv
import functions as fn

class Login():

    def __init__(self, master):
        
        self.master = master
        load_dotenv()

        self.master.title(fn.winTitle('Login'))
        self.master.iconbitmap('images/icon.ico')
        self.master.geometry('450x650')
        self.master.resizable(False, False)
        
        self.username = StringVar()
        self.password = StringVar()

        self.icon = ImageTk.PhotoImage(pilImage.open('images/icon.ico'))
        lbl_logo = ttk.Label(self.master, image=self.icon)
        content = ttk.Frame(self.master)

        lbl_title = ttk.Label(content, text=os.getenv("APP_TITLE"), font=("Segoe UI", 18, "bold")).pack()
        lbl_subtitle = ttk.Label(content, text=os.getenv("APP_SUBTITLE"), font=("Segoe UI", 14)).pack(pady=(0,20))
        lbl_username = ttk.Label(content, text="username or email address", font=("Segoe UI", 10))
        txt_username = ttk.Entry(content, textvariable=self.username)
        lbl_password = ttk.Label(content, text="password", font=("Segoe UI", 10))
        txt_password = ttk.Entry(content, textvariable=self.password, show="*")
        btn_submit = ttk.Button(content, text="Submit", command=self.validateUser)

        lbl_logo.pack(side=TOP)
        content.pack(side=BOTTOM, pady=50)
        lbl_username.pack(anchor=NW)
        txt_username.pack(fill=X, pady=(0,5))
        lbl_password.pack(anchor=NW)
        txt_password.pack(fill=X, pady=(0,5))
        btn_submit.pack(fill=X, pady=20)
        
    def validateUser(self):
        user = self.username.get()
        pswd = self.password.get()
        if user and pswd:
            if fn.isUserValidate(user, pswd):
                fn.createAuth(user)
                self.master.destroy()
                fn.startMain()
            else:
                fn.error("Please make sure that the details are correct!")
        else:
            fn.error("Please enter your login details!")

if __name__ == "__main__":
    fn.startMain()
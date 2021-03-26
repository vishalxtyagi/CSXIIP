from ttkwidgets.frames import ScrolledFrame
from ttkwidgets import Table
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image as pilImage
from functions import *
from ttkthemes import ThemedTk
import sqlite3, bcrypt
from dotenv import load_dotenv

load_dotenv()

class Dashboard():

    def __init__(self, db='school.db'):
        self.master = ThemedTk(background=True, theme="breeze")
        self.master.title('Dashboard | School Management System')
        self.master.iconbitmap('images/icon.ico')
        # self.master.state('zoomed')
        self.master.minsize(960, 550)
        
        titlelbl = Label(self.master,height=2, text='School Management System', font=("Segoe UI", 25, "bold"), bg="#1b2838",fg="white")
        menu = ScrolledFrame(self.master)

        self.conn = sqlite3.connect(db)  
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        for data in cur.fetchall():
            if data[0] == 'sqlite_sequence':
                pass
            else:
                menuimg = ImageTk.PhotoImage(pilImage.open("images/menu/"+ data[0] +".png").resize((50, 50), pilImage.ANTIALIAS))
                menubtn = ttk.Button(menu.interior, text=data[0], image=menuimg, compound=LEFT)
                menubtn.image = menuimg
                menubtn.pack()

        ctrl_frame = ttk.Frame(self.master)
        tbl_frame = ttk.Frame(self.master)
        mngr_frame = ttk.Frame(ctrl_frame)
        
        cur.execute("SELECT * FROM users")
        data_cols = [description[0] for description in cur.description]
        
        lbl_ctrls = ttk.Label(ctrl_frame, text='Manage Student', font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        for column in data_cols:
            if column == 'id':
                pass
            else:
                mng_frame = ttk.Frame(mngr_frame)
                mng_lbl = ttk.Label(mng_frame, text=column.replace('_', ' ').title(), font=("Segoe UI", 14)).pack(side=TOP, anchor=NW)
                mng_entry = ttk.Entry(mng_frame).pack(side=BOTTOM, fill=X, expand=True)
                mng_frame.pack(fill=X, pady=5)

        btn_list = ["add", "delete", "update", "clear"]
        for i in btn_list:
            btn = ttk.Button(mngr_frame, text=i).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)

        data_cols.remove('password')
        self.data_tbl = ttk.Treeview(tbl_frame, selectmode ='browse', columns=data_cols, show='headings')
        for col in data_cols:
            self.data_tbl.heading(col, text=col.replace('_', ' ').title())
        
        self.data_tbl.bind("<<TreeviewSelect>>", self.update_entry)

        cur.execute("SELECT "+ ",".join(data_cols) +" FROM users")
        tbl_result = cur.fetchall()
        for row in tbl_result:
            print(row) # it print all records in the database
            self.data_tbl.insert("", END, values=row)

        verscrlbar = ttk.Scrollbar(tbl_frame, orient='vertical', command=self.data_tbl.yview)
        horscrlbar = ttk.Scrollbar(tbl_frame, orient='horizontal', command=self.data_tbl.xview)
        verscrlbar.pack(side=RIGHT, fill=Y)
        horscrlbar.pack(side=BOTTOM, fill=X)
        self.data_tbl.configure(xscrollcommand = horscrlbar.set)
        self.data_tbl.configure(yscrollcommand = verscrlbar.set)

        titlelbl.pack(fill=X)
        menu.pack(side=LEFT, fill=BOTH, expand=True)
        ctrl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        mngr_frame.pack(fill=BOTH, expand=True, padx=20)
        tbl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        self.data_tbl.pack(fill=BOTH, expand=True)

    def update_entry(self):
        item = self.data_tbl.focus()
        print(self.data_tbl.item(item)["values"][0])

    def start(self):
        self.master.mainloop()

    def destroy(self):
        self.master.destroy()

if __name__ == '__main__':
    check_auth()
    
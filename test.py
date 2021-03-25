from ttkwidgets.frames import ScrolledFrame
from ttkwidgets import Table
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image as pilImage
from functions import *
import sqlite3, bcrypt

class Dashboard():

    def __init__(self,master, db='school.db'):
        self.master=master
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
        btn_frame = ttk.Frame(ctrl_frame)
        
        lbl_ctrls = ttk.Label(ctrl_frame, text='Manage Student', font=("Segoe UI", 14, "bold")).pack(pady=10)

        cur.execute("SELECT * FROM users")
        data_cols = []
        for description in cur.description:
            if description[0] == 'password':
                pass
            else:
                data_cols.append(description[0])
        data_tbl = Table(tbl_frame, columns=data_cols)
        for col in data_cols:
            data_tbl.heading(col, text=col)
            data_tbl.column(col, stretch=False)
        data_tbl.column(data_cols[0], type=int)

        for i in range(12):
            data_tbl.insert('', 'end', iid=i,
                        values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))

        titlelbl.pack(fill=X)
        menu.pack(fill=Y, side=LEFT)
        ctrl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        btn_frame.pack(side=BOTTOM, fill=X)
        tbl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        data_tbl.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    root = Tk()
    dashboard = Dashboard(root)
    root.mainloop()
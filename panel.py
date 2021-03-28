import os
from tkinter import *
from tkinter import ttk, messagebox
from ttkwidgets.frames import ScrolledFrame
from ttkwidgets import Table
from PIL import ImageTk
from PIL import Image as pilImage
from dotenv import load_dotenv
import functions as fn

class Panel():

    def __init__(self, master):
        
        self.page_name = "users"
        self.master = master
        load_dotenv()
        
        self.master.title(fn.winTitle('Dashboard'))
        self.master.iconbitmap('images/icon.ico')
        # self.master.state('zoomed')
        self.master.minsize(960, 550)
        
        lbl_title = Label(self.master,height=2, text='School Management System', font=("Segoe UI", 25, "bold"), bg="#1b2838",fg="white")
        menu_frame = ScrolledFrame(self.master)

        lst_menu = fn.getTablesFromDB()
        lst_menu[lst_menu.index('sqlite_sequence')] = 'dashboard'
        for data in lst_menu:
            menuimg = ImageTk.PhotoImage(pilImage.open("images/menu/"+ data +".png").resize((50, 50), pilImage.ANTIALIAS))
            menubtn = ttk.Button(menu_frame.interior, text=data, image=menuimg, compound=LEFT)
            menubtn.image = menuimg
            menubtn.pack()
        
        ctrl_frame = ttk.Frame(self.master)
        tbl_frame = ttk.Frame(self.master)
        mngr_frame = ttk.Frame(ctrl_frame)
        
        lbl_ctrls = ttk.Label(ctrl_frame, text='Manage Student', font=("Segoe UI", 14, "bold")).pack(pady=20)

        self.lst_entry = fn.getColumnsFromDB(self.page_name)
        self.lst_variables = []
        datatype = fn.getDataTypeFromTable(self.page_name)

        for column in self.lst_entry:
            if datatype[column] == 'TEXT': 
                entry_var = StringVar()
            else:
                entry_var = IntVar()
            mng_frame = ttk.Frame(mngr_frame)
            mng_lbl = ttk.Label(mng_frame, text=column.replace('_', ' ').title(), font=("Segoe UI", 14)).pack(side=TOP, anchor=NW)
            mng_entry = ttk.Entry(mng_frame, textvariable=entry_var).pack(side=BOTTOM, fill=X, expand=True)
            mng_frame.pack(fill=X, pady=5)
            self.lst_variables.append(entry_var)

        btn_add = ttk.Button(mngr_frame, text="add", command=fn.add()).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_delete = ttk.Button(mngr_frame, text="delete", command=self.delete_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_update = ttk.Button(mngr_frame, text="update", command=fn.update()).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_clear = ttk.Button(mngr_frame, text="clear", command=self.clear_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)

        self.tbl_cols = fn.getColumnsFromDB(self.page_name)
        if 'password' in self.tbl_cols:
            self.tbl_cols.remove('password')

        self.tbl_data = ttk.Treeview(tbl_frame, selectmode ='browse', columns=self.tbl_cols, show='headings')
        for col in self.tbl_cols:
            self.tbl_data.heading(col, text=col.replace('_', ' ').title())
        
        self.tbl_data.bind("<<TreeviewSelect>>", self.get_entry)

        for row in fn.fetchDataFromTable(",".join(self.tbl_cols), self.page_name):
            self.tbl_data.insert("", END, values=row)

        verscrlbar = ttk.Scrollbar(tbl_frame, orient='vertical', command=self.tbl_data.yview)
        horscrlbar = ttk.Scrollbar(tbl_frame, orient='horizontal', command=self.tbl_data.xview)
        verscrlbar.pack(side=RIGHT, fill=Y)
        horscrlbar.pack(side=BOTTOM, fill=X)
        self.tbl_data.configure(xscrollcommand = horscrlbar.set)
        self.tbl_data.configure(yscrollcommand = verscrlbar.set)

        lbl_title.pack(fill=X)
        menu_frame.pack(side=LEFT, fill=BOTH, expand=True)
        ctrl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        mngr_frame.pack(fill=BOTH, expand=True, padx=20)
        tbl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        self.tbl_data.pack(fill=BOTH, expand=True)

    def get_entry(self, event):
        item = self.tbl_data.focus()
        item_id = self.tbl_data.item(item)["values"][0]
        for i in range(len(self.lst_entry)):
            self.lst_variables[i].set("")
            if self.lst_entry[i] == 'password':
                pass
            else:
                data = fn.execSQL("SELECT " + self.lst_entry[i] + " FROM " + self.page_name + " WHERE id = " + str(item_id)).fetchone()
                self.lst_variables[i].set(data)

    def clear_entry(self):
        for i in range(len(self.lst_entry)):
            self.lst_variables[i].set("")
        for item in self.tbl_data.selection():
            self.tbl_data.selection_remove(item)
            

    def delete_entry(self):
        print(self.lst_variables)
        print(self.lst_variables[0])
        print(self.lst_variables[2].get())

        # fn.execSQL("DELETE FROM " + self.page_name + " WHERE id = " + item_id)

if __name__ == "__main__":
    fn.start(Panel)
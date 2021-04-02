import bcrypt, os
from functools import partial
from tkinter import *
from tkinter import ttk
from ttkwidgets.frames import ScrolledFrame
from PIL import ImageTk
from PIL import Image as pilImage
import functions as fn
from dotenv import load_dotenv

class Panel(Frame):
     
    def __init__(self, parent, controller, page_name):
         
        Frame.__init__(self, parent)
        
        load_dotenv()
        
        self.page_name = page_name

        lbl_title = Label(self,height=2, text=os.getenv("APP_TITLE"), font=("Segoe UI", 25, "bold"), bg="#1b2838",fg="white")
        menu_frame = ScrolledFrame(self)

        lst_menu = fn.fn.getMenuItems()
        lst_menu.append('empty')
        for data in lst_menu:
            menuimg = ImageTk.PhotoImage(pilImage.open("images/menu/"+ data +".png").resize((50, 50), pilImage.ANTIALIAS))
            menubtn = ttk.Button(menu_frame.interior, text=data, image=menuimg, compound=LEFT, command=partial(controller.show_frame,data))
            menubtn.image = menuimg
            menubtn.pack()

        lbl_title.pack(fill=X)
        menu_frame.pack(side=LEFT, fill=BOTH)

        if page_name not in fn.getTablesFromDB():
            self.customState()
        else:
            self.initApp()


    def customState(self):
        content = ttk.Frame(self)
        frm_state = ttk.Frame(content)

        if self.page_name == 'dashboard':
            image = ImageTk.PhotoImage(pilImage.open('images/overview.png').resize((150, 150), pilImage.ANTIALIAS))
            title = "Welcome Back, {}".format(fn.currentUser())
            subtitle = "<<< Browse the menu for more options."
        else:
            image = ImageTk.PhotoImage(pilImage.open('images/error.png').resize((150, 150), pilImage.ANTIALIAS))
            title = "Sorry! This service is currently unavailable"
            subtitle = "Please try again later or ask the developer for it."

        lbl_img = ttk.Label(frm_state, image=image)
        lbl_img.image = image
        lbl_title = ttk.Label(frm_state, text=title, font=("Segoe UI", 18, "bold"))
        lbl_subtitle = ttk.Label(frm_state, text=subtitle, font=("Segoe UI", 14))

        lbl_img.pack()
        lbl_title.pack()
        lbl_subtitle.pack(pady=(0,20))
        frm_state.place(relx=0.5, rely=0.5, anchor=CENTER)
        content.pack(side=LEFT, fill=BOTH, expand=True)

    def initApp(self):
        ctrl_frame = ScrolledFrame(self)
        tbl_frame = ttk.Frame(self)
        mngr_frame = ttk.Frame(ctrl_frame.interior)
        
        lbl_ctrls = ttk.Label(mngr_frame, text='Manage Student', font=("Segoe UI", 14, "bold")).pack(pady=20)

        self.lst_entry = fn.getColumnsFromTable(self.page_name)
        self.lst_variables = []

        for column in self.lst_entry:
            entry_var = StringVar()
            mng_frame = ttk.Frame(mngr_frame)
            mng_lbl = ttk.Label(mng_frame, text=column.replace('_', ' ').title(), font=("Segoe UI", 14)).pack(side=TOP, anchor=NW)
            if column == 'password':
                mng_entry = ttk.Entry(mng_frame, textvariable=entry_var, show="*").pack(side=BOTTOM, fill=X, expand=True)
            else:
                mng_entry = ttk.Entry(mng_frame, textvariable=entry_var).pack(side=BOTTOM, fill=X, expand=True)

            mng_frame.pack(fill=X, pady=5)
            self.lst_variables.append(entry_var)

        btn_add = ttk.Button(mngr_frame, text="add", command=self.add_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_delete = ttk.Button(mngr_frame, text="delete", command=self.delete_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_update = ttk.Button(mngr_frame, text="update", command=self.update_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)
        btn_clear = ttk.Button(mngr_frame, text="clear", command=self.clear_entry).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)

        self.tbl_cols = fn.getColumnsFromTable(self.page_name)
        if 'password' in self.tbl_cols:
            self.tbl_cols.remove('password')

        self.tbl_data = ttk.Treeview(tbl_frame, selectmode ='browse', columns=self.tbl_cols, show='headings')
        for col in self.tbl_cols:
            self.tbl_data.heading(col, text=col.replace('_', ' ').title())
        
        self.tbl_data.bind("<<TreeviewSelect>>", self.get_entry)

        self.show_data()

        verscrlbar = ttk.Scrollbar(tbl_frame, orient='vertical', command=self.tbl_data.yview)
        horscrlbar = ttk.Scrollbar(tbl_frame, orient='horizontal', command=self.tbl_data.xview)
        verscrlbar.pack(side=RIGHT, fill=Y)
        horscrlbar.pack(side=BOTTOM, fill=X)
        self.tbl_data.configure(xscrollcommand = horscrlbar.set)
        self.tbl_data.configure(yscrollcommand = verscrlbar.set)

        ctrl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        mngr_frame.pack(fill=BOTH, expand=True, padx=20)
        tbl_frame.pack(fill=BOTH, expand=True,side=LEFT)
        self.tbl_data.pack(fill=BOTH, expand=True)

    def show_data(self):
        self.tbl_data.delete(*self.tbl_data.get_children())
        for row in fn.fetchDataFromTable(",".join(self.tbl_cols), self.page_name):
            self.tbl_data.insert("", END, values=row)

    def get_entry(self, event):
        item = self.tbl_data.focus()
        item_id = self.tbl_data.item(item)["values"][0]
        for i in range(len(self.lst_entry)):
            self.lst_variables[i].set("")
            if self.lst_entry[i] == 'password':
                pass
            else:
                data = fn.fetchRecordFromTable(item_id, self.page_name, self.lst_entry[i])
                self.lst_variables[i].set(data[0])

    def clear_entry(self):
        for i in range(len(self.lst_entry)):
            self.lst_variables[i].set("")
        for item in self.tbl_data.selection():
            self.tbl_data.selection_remove(item)

    def delete_entry(self):
        if len(self.lst_variables[0].get()) > 0:
            item_id = self.lst_variables[0].get()
            if fn.fetchRecordFromTable(item_id, self.page_name) is not None:
                fn.deleteDataFromTable(item_id, self.page_name)
                self.show_data()
                self.clear_entry()
            else:
                fn.error("Record isn't exist with Id - {}".format(item_id))
        else:
            fn.error("Id field must be required!")

    def add_entry(self):
        dict_items = {}
        run_error = False
        for i in range(len(self.lst_entry)):
            if len(self.lst_variables[i].get()) > 0:
                if self.lst_entry[i] == 'password':
                    self.lst_variables[i].set(bcrypt.hashpw(self.lst_variables[i].get().encode(), bcrypt.gensalt()))
                dict_items[self.lst_entry[i]] = self.lst_variables[i].get()
            else:
                run_error = True
                fn.error("All field are required!")
                break
        if not run_error:
            fn.addDataToTable(dict_items, self.page_name)
            self.show_data()
            self.clear_entry()

    def update_entry(self):
        dict_items = {}
        run_error = False
        for i in range(len(self.lst_entry)):
            if len(self.lst_variables[i].get()) > 0:
                if i == 0:
                    pass
                if self.lst_entry[i] == 'password':
                    self.lst_variables[i].set(bcrypt.hashpw(self.lst_variables[i].get().encode(), bcrypt.gensalt()))
                dict_items[self.lst_entry[i]] = self.lst_variables[i].get()
            else:
                run_error = True
                fn.error("All field are required!")
                break
        if not run_error:
            fn.updateDataToTable(dict_items, self.lst_variables[0].get(), self.page_name)
            self.show_data()
            self.clear_entry()

if __name__ == "__main__":
    fn.startMain()
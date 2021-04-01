import tkinter as ttk
from ttkthemes import ThemedTk
import functions as fn
from login import Login
from panel import Panel
from dotenv import load_dotenv
import os

class MainApp(ThemedTk):
     
    def __init__(self):
        ThemedTk.__init__(self, background=True, theme="breeze")
        
        load_dotenv()

        self.title(os.getenv("APP_TITLE"))
        self.iconbitmap('images/icon.ico')
        # self.state('zoomed')
        self.minsize(960, 550)
        self.geometry("1024x550")

        container = ttk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}

        lst_table = fn.getTablesFromDB()
        lst_table[lst_table.index('sqlite_sequence')] = 'dashboard'
        for tbl in lst_table:
  
            frame = Panel(container, self, tbl)
            self.frames[tbl] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame("dashboard")

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.title(fn.winTitle(cont.title()))
        frame.tkraise()

if __name__ == '__main__':
    if fn.checkAuth():
        app = MainApp()
        app.mainloop()
    else:
        fn.start(Login)
    
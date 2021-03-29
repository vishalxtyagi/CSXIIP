import tkinter as tk 
import functions as fn
from login import Login
from panel import Panel

class MainApp(tk.Tk):
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
         
        container = tk.Frame(self)
        
        container.title(fn.winTitle('Dashboard'))
        container.iconbitmap('images/icon.ico')
        # container.state('zoomed')
        container.minsize(960, 550)

        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}

        for F in (Panel):
  
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Panel)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    if fn.checkAuth():
        app = MainApp()
        app.mainloop()
    else:
        fn.start(Login)
    
from ttkwidgets.frames import ScrolledFrame
from ttkwidgets import Table
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image as pilImage
from functions import *

dashboard = Tk()
dashboard.title('Dashboard | School Management System')
dashboard.iconbitmap('images/icon.ico')
# dashboard.state('zoomed')
dashboard.minsize(960, 550)

titlelbl = Label(dashboard,height=2, text='School Management System', font=("Segoe UI", 25, "bold"), bg="#1b2838",fg="white")
menu = ScrolledFrame(dashboard)
menulist = ['Dashboard', 'Student', 'Settings', 'Student', 'Settings', 'Student', 'Settings', 'Student', 'Settings', 'Student', 'Settings', 'Student', 'Settings']
for i in menulist:
    menuimg = ImageTk.PhotoImage(pilImage.open("images/menu/"+ i +".png").resize((50, 50), pilImage.ANTIALIAS))
    menubtn = ttk.Button(menu.interior, text=i, image=menuimg, compound=LEFT)
    menubtn.image = menuimg
    menubtn.pack()

content = ttk.Frame(dashboard)
data = ttk.Frame(dashboard)
btnframe = ttk.Frame(content)

contentlbl = ttk.Label(content, text='Manage Student', font=("Segoe UI", 14, "bold")).pack(pady=10)

managelist = ['name', 'email', 'phone']
for i in managelist:
    fram = ttk.Frame(content)
    lbl = ttk.Label(fram, text=i, font=("Segoe UI", 14)).pack(side=LEFT, padx=10)
    entry = ttk.Entry(fram).pack(side=LEFT,fill=X, expand=True, padx=10)
    fram.pack(fill=X, padx=20)
  
btnlist = ["add", "delete", "update", "clear"]
for i in btnlist:
    btn = ttk.Button(btnframe, text=i).pack(side=LEFT,fill=X, expand=True, padx=5, pady=30)

columns = ["A", "B"]
datatbl = Table(data, columns=columns)
for col in columns:
    datatbl.heading(col, text=col)
    datatbl.column(col, width=100, stretch=False)
datatbl.column('A', type=int)

for i in range(12):
    datatbl.insert('', 'end', iid=i,
                 values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))


titlelbl.pack(fill=X)
menu.pack(fill=Y, side=LEFT)
content.pack(fill=BOTH, expand=True,side=LEFT)
btnframe.pack(side=BOTTOM, fill=X)
data.pack(fill=BOTH, expand=True,side=LEFT)
datatbl.pack(fill=BOTH, expand=True)

dashboard.mainloop()

from tkinter import *

root = Tk()
root.geometry('1300x700')
root.configure(bg = 'light blue')

#frame = Frame(root)

#frame.pack(side = TOP)

button = Button(root, text = 'Browse an image ',bg = 'red',fg = 'yellow').place(x=100,y=50)

label = Label(root, text="weapon detection and criminal face identification",bg = 'yellow',fg = 'red',font=("Courier",14,"bold")).place(x=50,y=30)




root.mainloop()

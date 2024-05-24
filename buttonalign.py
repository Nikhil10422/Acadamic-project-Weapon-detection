# import everything from tkinter module
from tkinter import *

#create a tkinter window
root = Tk()

root.title('HI')
#open window having dimension 100x100
root.geometry('300x300')

#create a button
btn = Button(root, text = 'click me !', bd = '2',command = root.destroy)
                            

#set the position of button on the top of window
btn.pack(side='left')

root.mainloop()

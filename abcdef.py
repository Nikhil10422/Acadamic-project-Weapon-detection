import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    filename = filedialog.askopenfilename()
    if filename:
        print("selected file:",filename)

root = tk.Tk()

button = tk.Button(root, text="Open File", command=open_file_dialog)
button.pack()

root.mainloop()
        

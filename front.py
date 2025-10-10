import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image,ImageTk


def on_button_click():
    label.config(text="Hello!")

def my_upload(): # show file browser and preview of photo
    global filename,img
    f_types = [('All Files', '*.*'), 
             ('JPG', '*.jpg'),
             ('PNG', '*.png')              ]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img=ImageTk.PhotoImage(file=filename)
    b3=tk.Button(root,image=img) # display image on this
    b3.pack()
def my_add():
    pass # code to store data in database

root = tk.Tk()
root.title("AI Image Captioner")
root.geometry("500x400")

label = tk.Label(root, text="Please Input Video")
label.pack(pady=20)

#button = tk.Button(root, text="Click me", command=on_button_click)
#button.pack()

b1=tk.Button(root,text='Upload',command=lambda:my_upload())
b1.pack(side=tk.RIGHT, padx=10, pady=5)

b2=tk.Button(root,text='Enter',command=lambda:my_add())

b2.pack(side=tk.LEFT, padx=10, pady=5)

result = tk.Label(root, text = 'The caption will go here')
result.pack(side = tk.BOTTOM, padx = 20, pady = 15)

global filename,img

root.mainloop()


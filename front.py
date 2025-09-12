import tkinter as tk

def on_button_click():
    label.config(text="Hello!")

root = tk.Tk()
root.title("AI Image Captioner")
root.geometry("500x400")

label = tk.Label(root, text="")
label.pack(pady=20)

button = tk.Button(root, text="Click me", command=on_button_click)
button.pack()

root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image,ImageTk
import os
import shutil
import cv2



INPUT_FOLDER = "shared_input"
UPLOAD_STACK = []  # This will behave like a stack
os.makedirs(INPUT_FOLDER, exist_ok=True)


def on_button_click():
    label.config(text="Hello!")

root = tk.Tk()
root.title("AI Image Recognizer")
root.geometry("600x600")

img_label = tk.Label(root)
img_label.pack()

result_label = tk.Label(root, text="Upload an image or video to analyze.", wraplength=400)
result_label.pack(pady=15)

filename = None

def my_upload(): # show file browser and preview of photo
    global filename,img, UPLOAD_STACK
    f_types = [('All Files', '*.*'),
        ('JPG', '*.jpg'),
        ('PNG', '*.png'),
        ('MP4', '*.mp4'),
        ('MOV', '*.mov'),
        ('AVI', '*.avi')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if not filename:
        return

    # Copy to shared_input for backend access
    dest_path = os.path.join(INPUT_FOLDER, os.path.basename(filename))
    shutil.copy(filename, dest_path)
    UPLOAD_STACK.append(dest_path)

    # Determine file type
    ext = filename.lower().split('.')[-1]

    if ext in ("jpg", "jpeg", "png"):
        # --- Image preview ---
        img = Image.open(filename)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk, text="")
        img_label.image = img_tk

    elif ext in ("mp4", "mov", "avi", "mkv"):
        # --- Video thumbnail (extract first frame) ---
        cap = cv2.VideoCapture(filename)
        frame_num = 1  # pick the 2th frame
        success = False
        for _ in range(frame_num):
            success, frame = cap.read()
            if not success:
                break
        cap.release()
        if success:
            # Convert from BGR (OpenCV) to RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img.thumbnail((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk, text="")
            img_label.image = img_tk
        else:
            img_label.config(text="Could not read video frame", image="")
    else:
        img_label.config(text="Unsupported file type", image="")

def my_add():
    """Check if backend has processed the file"""
    output_path = os.path.join(INPUT_FOLDER, "result.json")
    if not os.path.exists(output_path):
        result_label.config(text="Waiting for backend to process...")
        root.after(2000, my_add)  # check again after 2s
    else:
        with open(output_path, "r") as f:
            data = json.load(f)
        caption = data.get("caption", "No caption found.")
        detections = data.get("detections", "No detections found.")
        result_label.config(text=f"Caption: {caption}\nDetections: {detections}")
        os.remove(output_path)  # clear old results
 # code to store data in database



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

global img

root.mainloop()


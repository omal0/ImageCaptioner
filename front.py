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

root.configure(bg="#ECF0F1") # maybe remove 




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
        frame_num = 1  # pick the 1st frame
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


style = ttk.Style()
style.theme_use("clam")

# --- Button styles ---
style.configure("Upload.TButton",
                font=("Helvetica", 12, "bold"),
                padding=8,
                background="#3498DB",
                foreground="white")

style.map("Upload.TButton",
          background=[("active", "#2980B9")])

style.configure("Enter.TButton",
                font=("Helvetica", 12, "bold"),
                padding=8,
                background="#2ECC71",
                foreground="white")

style.map("Enter.TButton",
          background=[("active", "#27AE60")])

# --- Label styles ---
style.configure("Header.TLabel",
                font=("Helvetica", 18, "bold"),
                background="#ECF0F1",
                foreground="#2C3E50")

style.configure("Result.TLabel",
                font=("Helvetica", 12),
                background="#ECF0F1",
                foreground="#34495E")

# --- UI Layout ---
header = ttk.Label(root, text="AI Image & Video Analyzer", style="Header.TLabel")
header.pack(pady=15)

#img_label = tk.Label(root, bg="#BDC3C7", width=300, height=200)
#img_label.pack(pady=10)

result_label = ttk.Label(root, text="Upload an image or video to analyze.",
                         style="Result.TLabel", wraplength=450)
result_label.pack(pady=15)

# Buttons grouped in a frame
button_frame = tk.Frame(root, bg="#ECF0F1")
button_frame.pack(pady=10)

b1 = ttk.Button(button_frame, text="Upload", style="Upload.TButton", command=lambda: my_upload())
b1.pack(side=tk.LEFT, padx=10)

b2 = ttk.Button(button_frame, text="Analyze", style="Enter.TButton", command=lambda: my_add())
b2.pack(side=tk.LEFT, padx=10)

img_label = tk.Label(root)
img_label.pack()

global img

root.mainloop()


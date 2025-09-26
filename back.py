# install once in your environment:
# pip install ultralytics opencv-python
from ultralytics import YOLO
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load YOLOv8 model on GPU
model = YOLO("model/yolo11x.pt").to(device)
# Load this if you dont have cuda
# model = YOLO("model/yolo11x.pt")

# Run prediction on an image
results = model("TestFootage/carspassingby.mp4", show=True)  # show=True opens a window with boxes

# Print detailed results
for result in results:
    boxes = result.boxes
    for box in boxes:
        print(f"Class: {model.keypoints[int(box.cls)]}, "
              f"Conf: {float(box.conf):.2f}, "
              f"Box: {box.xyxy.tolist()}")
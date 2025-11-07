# install once in your environment:
# pip install ultralytics opencv-python
from ultralytics import YOLO
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load YOLOv8 model on GPU
if device == "cuda":
    yolomodel = YOLO("model/yolo11x.pt").to(device)
elif device == "cpu":
    yolomodel = YOLO("model/yolo11n.pt").to(device)

# Run prediction on an image
results = yolomodel("TestFootage/carspassingby.mp4", show=True)  # show=True opens a window with boxes

# Print detailed results
for result in results:
    boxes = result.boxes
    for box in boxes:
        print(f"Class: {model.keypoints[int(box.cls)]}, "
              f"Conf: {float(box.conf):.2f}, "
              f"Box: {box.xyxy.tolist()}")
        
# Blip Processing
# processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
# blipmodel = 
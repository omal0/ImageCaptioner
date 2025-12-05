# install once in your environment:
# pip install ultralytics opencv-python
from ultralytics import YOLO
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load YOLOv8 model on GPU
if device == "cuda":
    yolomodel = YOLO("model/yolo11x.pt").to(device)
elif device == "cpu":
    yolomodel = YOLO("model/yolo11n.pt").to(device)

# Run prediction on an image
# results = yolomodel("TestFootage/carspassingby.mp4", show=True)  # show=True opens a window with boxes
video_path = "TestFootage/carspassingby.mp4"
cap = cv2.VideoCapture(video_path)
frame_num = 0

# Blip Processing
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(frame):
    # Downscale before BLIP
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = image.resize((384, 384))

    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.inference_mode():
        out = blip_model.generate(
            **inputs,
            max_new_tokens=20
        )
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

if not cap.isOpened():
    print("Error")
else:
    print("Start")

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_num += 1

        # Yolo results
        results = yolomodel(frame, show=True)  # show=True opens a window with boxes 

        # Blip Captions for frame
        if frame_num % 10 == 0:
            full_frame_caption = describe_image(frame)
            print(f"Frame {frame_num}: {full_frame_caption}")

        for result in results:
            boxes = result.boxes

            for box in boxes:
                cls_id = int(box.cls)
                conf = float(box.conf)
                bbox = box.xyxy.tolist()
                cls_name = yolomodel.names[cls_id]  # class name from YOLO model

        print(f"Class: {cls_name}, Conf: {conf:.2f}, Box: {bbox}")


        # for result in results:

        #     boxes = result.boxes

        #     for box in boxes:
        #        print(f"Class: {model.keypoints[int(box.cls)]}, "
        #        f"Conf: {float(box.conf):.2f}, "
        #        f"Box: {box.xyxy.tolist()}")

    cap.release()
    cv2.destroyAllWindows()

print("Done")


# # Print detailed results
# for result in results:

#     boxes = result.boxes
    
#     # Drawing boxes on video
#     for box in boxes:

#         print(f"Class: {model.keypoints[int(box.cls)]}, "
#               f"Conf: {float(box.conf):.2f}, "
#               f"Box: {box.xyxy.tolist()}")
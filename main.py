import cv2 # using opencv for image capturing

# putting video file into object to be manipulated
test = cv2.VideoCapture("TestFootage/carspassingby.mp4")

# sets the frame we want to look at
test.set(cv2.CAP_PROP_POS_FRAMES, 9)

# reads the frame at the new position, ret is a boolean to test if the
# VideoCapture object was actually done, frame is the actual frame if it worked
ret, frame = test.read()

# checking if .read() actually did anything
if ret:
    # saves frame to image file in Frames folder
    cv2.imwrite("TestFootage/Frames/cartestframe10.jpg", frame)

# stop working with video
test.release()

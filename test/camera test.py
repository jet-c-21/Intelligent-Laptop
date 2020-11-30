import time

import cv2
import imutils
from imutils.video import VideoStream

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0

while True:
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

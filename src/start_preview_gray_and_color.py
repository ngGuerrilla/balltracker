import numpy as np
import cv2
from picamera2 import Picamera2

cv2.startWindowThread()

# cap = cv2.VideoCapture(0)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

while(True):
    # ret, frame = cap.read()
    frame = picam2.capture_array()
    #frame = cv2.flip(frame, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cap.release()
cv2.destroyAllWindows()
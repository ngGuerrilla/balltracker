from picamera2 import Picamera2, Preview
import time

# import cv2
# print(cv2.__version__)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(5)
picam2.capture_file('test_image2.jpg')

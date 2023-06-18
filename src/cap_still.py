#!/usr/bin/python3

from picamera2 import Picamera2
from time import sleep
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1440, 1080)})
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 35000, "AnalogueGain": 6.0})

# Get current date and time
now = datetime.now()
# Format as string in the format YearMonthDay-HourMinuteSecond
dt_string = now.strftime("%Y%m%d-%H%M%S")
filename = "/home/csander180/Desktop/Images/img_" + dt_string + ".jpg"

picam2.start()
picam2.capture_file(filename)
picam2.stop()
#!/usr/bin/python3

from time import sleep
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
only_mode = picam2.sensor_modes[0]
picam2.video_configuration = picam2.create_video_configuration(
    raw={"size": only_mode["size"], "format": only_mode["format"].format}
)
picam2.configure("video")
picam2.set_controls({"FrameRate": only_mode["fps"]})
# picam2.set_controls({"ExposureTime": 16666, "AnalogueGain": 10.0})
# Hardware H264 encoding support recommended. Tested on Pi 4B 1GB
encoder_config = H264Encoder()

# Get current date and time
now = datetime.now()
# Format as string in the format YearMonthDay-HourMinuteSecond
dt_string = now.strftime("%Y%m%d-%H%M%S")
filename = "/home/csander180/Desktop/Videos/vid_" + dt_string + ".mp4"

output_file = FfmpegOutput(filename)
# Start a Null preview to avoid 1-2 second record delay else use continuous
picam2.start_recording(encoder_config, output_file, quality=Quality.HIGH)
sleep(5)
picam2.stop_recording()

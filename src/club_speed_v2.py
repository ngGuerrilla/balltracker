import cv2
from picamera2 import Picamera2
# from picamera2.array import PiRGBArray
import numpy as np
import time

def detect_club(image):
    # Threshold the image to get a binary image
    _, thresholded = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate the center of the largest contour
    moments = cv2.moments(largest_contour)
    cx = int(moments['m10']/moments['m00'])
    cy = int(moments['m01']/moments['m00'])

    return (cx, cy)

def calculate_club_speed(previous_position, current_position, time_between_frames, inchPerPixel, fps):
    # Calculate the distance between the previous and current positions
    dx = current_position[0] - previous_position[0]
    dy = current_position[1] - previous_position[1]
    distance = np.sqrt(dx*dx + dy*dy)

    # Divide by the time between frames to get speed
    #speed = distance / time_between_frames
    speed = distance * inchPerPixel * fps
    speed = speed * 0.057

    return speed


# Initialize the camera
camera = Picamera2()
#camera.resolution = (640, 480)  # Set the resolution that works for you
#camera.framerate = 60  # Capture at a high frame rate
#rawCapture = PiRGBArray(camera, size=(640, 480))
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

# Allow the camera to warm up
time.sleep(2)

# Initialize variables to hold the previous and current club positions
previous_club_position = None
current_club_position = None

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True:
    # Grab the raw NumPy array representing the image
    #image = frame.array
    image = camera.capture_array()
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the club in the image (this will depend on your specific club and lighting conditions)
    # You might want to use a technique like template matching, feature detection, or machine learning
    club_position = detect_club(gray)

    # If this is the first frame, initialize the previous and current club positions
    if previous_club_position is None and current_club_position is None:
        previous_club_position = club_position
        current_club_position = club_position
    else:
        # Update the club positions
        previous_club_position = current_club_position
        current_club_position = club_position

        # Calculate the club speed
        inchPerPixel = 0.0804
        fps = 60
        club_speed = calculate_club_speed(previous_club_position, current_club_position, 0.01666666666, inchPerPixel, fps)
        # print("Club speed: ", club_speed)
        
        # Overlay the club speed on the image
        cv2.putText(image, f"Club speed: {club_speed:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the image
        cv2.imshow('Image with Club Speed', image)
        cv2.waitKey(1)
    # Clear the stream in preparation for the next frame
    #rawCapture.truncate(0)
    
camera.stop()
cv2.destroyAllWindows()

from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from picamera2 import Picamera2
from datetime import datetime

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points

# White golf ball
# colorLower = (-10, 100, 100)  # (24, 100, 100)
# colorUpper = (10, 255, 255)  # (44, 255, 255)

# Red golf ball
colorLower = (168, 100, 100)  # (24, 100, 100)
colorUpper = (188, 255, 255)  # (44, 255, 255)

# Yellow foam ball
# colorLower = (19, 100, 100)  # (24, 100, 100)
# colorUpper = (39, 255, 255)  # (44, 255, 255)

pts = deque(maxlen=args["buffer"])

cv2.startWindowThread()

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    # camera = cv2.VideoCapture(0)
    camera = Picamera2()
    camera.configure(
        camera.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
    )
    camera.start()

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# Get current date and time
now = datetime.now()
# Format as string in the format YearMonthDay-HourMinuteSecond
dt_string = now.strftime("%Y%m%d-%H%M%S")
filename = "/home/csander180/Desktop/Videos/ball_tracking_" + dt_string + ".avi"

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename,fourcc, 20.0, (640,480))

# keep looping
while True:
    # grab the current frame
    # (grabbed, frame) = camera.read()

    if not args.get("video", False):
        frame = camera.capture_array()
        grabbed = False

    else:
        (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space
    
    # frame = imutils.resize(frame, width=600)
    # frame = imutils.rotate(frame, angle=180)
    
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # write the frame
    out.write(frame)
    
    # show the frame to our screen
    #cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Frame", frame)

    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

# cleanup the camera and close any open windows
if args.get("video", False):
    camera.release()
else:
    camera.stop()
out.release()
cv2.destroyAllWindows()

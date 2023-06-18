import cv2
import numpy as np

# known parameters
KNOWN_WIDTH =  1.68 # the actual width of the object in inches
KNOWN_DISTANCE =  69.5625 # the reference distance in inches
KNOWN_PIXEL_WIDTH =  107.34 # 49.07 # (640x480)  | 111.63 (if using 1456x1088) # the apparent width of the object in the reference image in pixels

# calculate the focal length
focal_length = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
print(f'focal_length: {focal_length}')
# run 2: focal_length = 4622.1796875
# run 3: focal_length = 2031.8046875000002

# load the image you want to measure
image = cv2.imread('test_image2.jpg')

# convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of red color in HSV
# lower_red = np.array([0, 100, 100])
# upper_red = np.array([10, 255, 255])
lower_red = np.array([168, 100, 100])
upper_red = np.array([188, 255, 255])

# threshold the HSV image to get only red colors
mask_red = cv2.inRange(hsv, lower_red, upper_red)

# define range of green color in HSV
# lower_green = np.array([36, 0, 0])
# upper_green = np.array([86, 255, 255])

# threshold the HSV image to get only green colors
# mask_green = cv2.inRange(hsv, lower_green, upper_green)

# define range of yellow color in HSV
# lower_yellow = np.array([20, 100, 100])
# upper_yellow = np.array([30, 255, 255])

# threshold the HSV image to get only yellow colors
# mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

# combine the three masks
# mask = cv2.bitwise_or(mask_red, mask_green, mask_yellow)

# find contours in the mask
contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find the largest contour
largest_contour = max(contours, key = cv2.contourArea)

# get the bounding rectangle for the largest contour
x, y, w, h = cv2.boundingRect(largest_contour)

# the width of the bounding rectangle is the pixel width of the object
object_pixel_width = w

# calculate the distance to the object
distance = (KNOWN_WIDTH * focal_length) / object_pixel_width
print(f'Distance to object: {distance}')

# 1st run (with only green and red) resulted in 554.6615625000001
# 2nd run very similar (green, red and yellow)
# 3rd run resulted in 243.8165625

# The resulting distance is in the same units as the known distance and known width, which in the given script are inches.

# So, if KNOWN_WIDTH and KNOWN_DISTANCE are in inches, the resulting distance will also be in inches.

# In general, the units of the calculated distance will match the units of the actual width of the object (KNOWN_WIDTH) and the reference distance (KNOWN_DISTANCE).
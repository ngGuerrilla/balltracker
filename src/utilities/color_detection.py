import cv2
import numpy as np

# Read the picure - The 1 means we want the image in BGR
img = cv2.imread('/home/csander180/Desktop/test2.jpg', 1) 

# resize imag to 20% in each axis
img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
# convert BGR image to a HSV image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

# NumPy to create arrays to hold lower and upper range 
# The “dtype = np.uint8” means that data type is an 8 bit integer

# Red Golf Ball
# lower_range = np.array([168, 100, 100], dtype=np.uint8) 
# upper_range = np.array([188, 255, 255], dtype=np.uint8)

# Yellow foam ball
lower_range = np.array([19, 100, 100], dtype=np.uint8) 
upper_range = np.array([39, 255, 255], dtype=np.uint8)

# create a mask for image
mask = cv2.inRange(hsv, lower_range, upper_range)

# display both the mask and the image side-by-side
cv2.imshow('mask',mask)
cv2.imshow('image', img)

# wait to user to press [ ESC ]
while(1):
  k = cv2.waitKey(0)
  if(k == 27):
    break
 
cv2.destroyAllWindows()
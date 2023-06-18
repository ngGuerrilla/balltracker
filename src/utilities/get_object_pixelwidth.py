import math

# known parameters
focal_length = 35  # in mm
distance = 69.5625  # in inches, convert to mm
distance *= 25.4  # mm/inch
actual_width = 1.68  # in inches, convert to mm
actual_width *= 25.4  # mm/inch
sensor_diagonal = 6.3  # in mm
image_resolution_width = 640  # in pixels
image_resolution_height = 480  # in pixels

# calculate sensor width and height based on 4:3 aspect ratio
x = sensor_diagonal / math.sqrt(4**2 + 3**2)
sensor_width = 4 * x
sensor_height = 3 * x

# calculate image size on sensor (in mm)
image_size = (actual_width * focal_length) / distance

# calculate pixel size
pixel_width = image_size * (image_resolution_width / sensor_width)

print('The object will span approximately {:.2f} pixels in width.'.format(pixel_width))

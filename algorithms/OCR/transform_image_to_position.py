PIXELSX = 1536
PIXELSY = 2048

CMX = 21
CMY = 29.7

px_x_cm = PIXELSX / CMX
px_y_cm = PIXELSY / CMY

def transform_image_to_position(x,y):
    x_robot = x / px_x_cm
    y_robot = y / px_y_cm

    return x_robot, y_robot

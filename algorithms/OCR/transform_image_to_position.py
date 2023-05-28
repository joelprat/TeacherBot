PIXELSX = 2250
PIXELSY = 4000

CMX = 29.7
CMY = 21

px_x_cm = PIXELSX / CMX
px_y_cm = PIXELSY / CMY

def transform_image_to_position(x,y):
    x_robot = x / px_x_cm
    y_robot = y / px_y_cm

    return x_robot, y_robot

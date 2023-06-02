PIXELSX = 3264
PIXELSY = 2448

CMX = 21
CMY = 29.7

px_x_cm = PIXELSX / CMX
px_y_cm = PIXELSY / CMY

#tener en quenta que el eje de cordenadas para la foto esta invertido respecto el del robot
def transform_image_to_position(x,y):
    #print("X antes",x/ px_x_cm)
    #print("y antes",y/ px_y_cm)
    y_robot  = x / px_x_cm  - 19  #sumamos la diferencia desde el punto y
    x_robot = - y / px_y_cm +  28 #sumamos la diferencia desde el punto x
    return x_robot, y_robot


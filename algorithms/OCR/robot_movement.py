import text_recognition
import transform_image_to_position

from sympy.physics.mechanics import dynamicsymbols
from sympy import *
import numpy as np

LA = 20
LB = 20
LC = 9.5

STEPS = 4

theta1, theta2 = dynamicsymbols('theta1 theta2')


# {'CARLLES': [728, 1329, 807, 1753], 'LLAMO': [727, 944, 814, 1257], 'HOLLA': [724, 182, 838, 598]}
def calculation_move_for_word(palabras):
    # movs = {palabra: [xinicial, altura para tachar, longitud de los steps]}
    movs = {}
    for palabra in palabras:
        coord = palabras[palabra]
        x = coord[0] 
        y = coord[1] 
        w = coord[2]
        h = coord[3]

        y = y - h/2
        movs[palabra] = [x, y, w/STEPS]
        
    return movs


def set_equations(movs):

    angulos = []
    for mov in movs:
        angulo = []
        for i in range(STEPS):
            #print("pixels XY")
            #print(movs[mov][0], movs[mov][1])
            x_robot, y_robot = transform_image_to_position.transform_image_to_position(movs[mov][0], movs[mov][1])
            x_robot = round(x_robot,3)
            y_robot = round(y_robot + 15 ,3)
            #print("xyrobot")
            #print(x_robot, y_robot)
            angulo.append(move_arms(x_robot, y_robot))
            movs[mov][0] += movs[mov][2]
            print(x_robot)
        print("------------- Cambio palabra ------------- \n")        
        angulos.append(angulo)
    
    #angulos = [//palabra1[angulos1,angulos2,angulos3,angulos4], //palabra2[angulos1,angulos2,angulos3,angulos4]...]
    return angulos


def move_arms(x, y):
    #x = 40
    #y = 40
    eq1 = (LA * cos(theta1) + LB * cos(theta1 + theta2)) - x
    eq2 = (LA * sin(theta1) + LB * sin(theta1 + theta2)) - y
    #eq3 = 10 - LC - 0

    try:
        q = nsolve((eq1, eq2), (theta1, theta2), (1,1), prec=5)
    except Exception as e:
        print("Error:", str(e))
        q = [0, 0, 0, 0]

    q[0] = q[0] - round(q[0] / (np.pi * 2)) * 2 * np.pi
    q[1] = q[1] - round(q[1] / (np.pi * 2)) * 2 * np.pi

    q[0] = q[0] * 180 / np.pi
    q[1] = q[1] * 180 / np.pi

    return q


#main
def robot_movement():
    palabras = text_recognition.text_recognition()
    print(palabras)
    movs = calculation_move_for_word(palabras)
    #movs = calculation_move_for_word({'CARLLES': [728, 1329, 79, 424], 'LLAMO': [727, 944, 87, 313], 'HOLLA': [724, 182, 114, 416]})
    angulos = set_equations(movs)
    print("--------------------------------\n")
    print(angulos)

    return angulos


robot_movement()
    
# 2250x4000
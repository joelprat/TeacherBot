import text_recognition
import transform_image_to_position

from sympy.physics.mechanics import dynamicsymbols
from sympy import *
import numpy as np

LA = 20
LB = 20
LC = 9.5

theta1, theta2 = dynamicsymbols('theta1 theta2')

def set_equations(movs):

    angulos = []
    for mov in movs:
        angulo = []        
        for i in mov['bounding_box']:                     
            x_robot, y_robot = transform_image_to_position.transform_image_to_position(i[0],i[1])
            x_robot = round(x_robot,3)
            y_robot = round(y_robot ,3)                       
            #print("x:",str(x_robot))
            #print("y:",str(y_robot))            
            angulo.append(move_arms(x_robot, y_robot))           
            angulos.append(angulo)
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

    q[0] = round(q[0] * 180 / np.pi,2)
    q[1] = round(q[1] * 180 / np.pi,2)

    return q



def robot_movement():
    palabras = text_recognition.text_recognition()    
    angulos = set_equations(palabras)   
    #print(angulos)

    return angulos

#robot_movement()
    
# 2250x4000
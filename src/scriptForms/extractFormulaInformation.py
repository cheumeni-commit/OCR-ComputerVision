import cv2
import numpy as np

from src.constants import (c_SCALE,
                           c_COUNT_1,
                           c_COUNT_2
                           )

c_CIRCLE = []
c_POINT1 = []
c_POINT2 = []
c_MYPOINTS = []
c_COLOR = []


def pressPoint(event, x, y):

    global c_COUNT_1, c_POINT1, c_POINT2, c_COUNT_2, c_CIRCLE, c_COLOR

    if event == cv2.EVENT_LBUTTONDOWN:
        if c_COUNT_1 == 0:
            c_POINT1 = int(x//c_SCALE), int(y//c_SCALE)
            c_COUNT_1 +=1
            color = (np.random.randint(0,2)*200, np.random.randint(0,2)*200, np.random.randint(0,2)*200)
        elif c_COUNT_1 == 1:
            c_POINT2 = int(x//c_SCALE), int(y//c_SCALE)
            type = input('Entree type') # nombre, string etc..
            name = input('Entre le nom') # nom, prenom profession etc..
            c_MYPOINTS.append([c_POINT1, c_POINT2, type, name])
            c_COUNT_1 = 0
        c_CIRCLE.append([x, y, color])
        c_COUNT_2 += 1

images = cv2.imread('../data/poster/affiche 2.jpg')
images = cv2.resize(images, (0, 0), None, c_SCALE, c_SCALE)

while True:
    for x,y, color in c_CIRCLE:
        cv2.circle(images, (x,y), 3, color, cv2.FILLED)
    cv2.imshow('oi', images)
    cv2.setMouseCallback('oi', pressPoint)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(c_MYPOINTS)
        break
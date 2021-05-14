# Computer Vision
# Extraction d'information sur des images
# Author : JM Cheumeni
import cv2
import numpy as np
import os
import time
import random




scale = 1
circle = []
count = 0
count2 = 0
pts1 = []
pts2 = []
myPoints = []
color = []

def pressPoint(event, x, y, flags, params):

     global count, pts1, pts2, count2, circle, color

     if event == cv2.EVENT_LBUTTONDOWN:
         if count == 0:
             pts1 = int(x//scale), int(y//scale)
             count +=1
             color = (np.random.randint(0,2)*200, np.random.randint(0,2)*200, np.random.randint(0,2)*200)
         elif count == 1:
             pts2 = int(x//scale), int(y//scale)
             type = input('Entree type') # nombre, string etc..
             name = input('Entre le nom') # nom, prenom profession etc..
             myPoints.append([pts1, pts2, type, name])
             count = 0
         circle.append([x, y, color])
         count2 += 1

images = cv2.imread('../data/poster/affiche 2.jpg')
images = cv2.resize(images, (0, 0), None, scale, scale)

while True:
    for x,y, color in circle:
        cv2.circle(images, (x,y), 3, color, cv2.FILLED)
    cv2.imshow('oi', images)
    cv2.setMouseCallback('oi', pressPoint)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(myPoints)
        break
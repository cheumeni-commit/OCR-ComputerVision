# Computer Vision
# Extraction d'information sur des images
# Author : JM Cheumeni

import cv2
import numpy as np
import os
import time
import random
import pytesseract
from pytesseract import *

class extracInformationOfformula():

    def __init__(self, roi, pixelsTreshold):

        self.roi = roi
        self.pixelsTreshold = pixelsTreshold

    def analyseImages(self, images):
        '''

        :param images: traitement des images
        :return: donnees extraites et l'image avec le mask
        '''

        imgShow = images.copy()
        imgMask = np.zeros_like(imgShow)
        data = []
        for x, r in enumerate(self.roi):

            cv2.rectangle(imgMask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0,255,0), cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 2, 0)
            # cropping des region d'interet : ROI
            imgCrop = images[r[0][1]:r[1][1], r[0][0]:r[1][0]]
            #cv2.imshow(str(x), imgCrop)

            if r[2] == 'text':
                 print(f'{r[3]} : {pytesseract.image_to_string(imgCrop)}')
                 data.append(pytesseract.image_to_string(imgCrop, lang='fra').strip())
            if r[2] == 'box':
               imgGray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
               imgThesh = cv2.threshold(imgGray, 170,255, cv2.THRESH_BINARY_INV)[1]
               totalPixels = cv2.countNonZero(imgThesh)
               #print(totalPixels)
               if totalPixels>pixelsTreshold :
                   totalPixels = "oui"
               else:
                   totalPixels = "non"
               print(f'{r[3]} : {totalPixels}')
               data.append(totalPixels.strip())

        return data, imgShow

    def saveDataForCsv(self, nameFile, data):
        '''

        :param nameFile: fichier de sortie des donnees (.csv)
        :param data: donnees a stocker dans le fichier
        :return:
        '''

        with open(nameFile, 'a') as f:
            f.write((str(0) + ';'))
            for i in range(len(data)):
                if i < len(data) -1:
                    f.write((str(data[i])+';'))
                else:
                    f.write(str(data[i]))
            f.write('\n')

if __name__ == "__main__":

    ################################# ROI et seuils ###################"
    pixelsTreshold = 100
    roi = [[(267, 553), (1196, 614), 'text', 'nom'],
           [(1397, 547), (2273, 602), 'text', 'prenom'],
           [(349, 744), (1163, 785), 'text', 'nationalite'],
           [(1437, 733), (2272, 788), 'text', 'profession'],
           [(420, 1275), (638, 1334), 'text', 'taille'],
           [(2073, 1493), (2120, 1543), 'box', 'pension_invalidite'],
           [(1107, 1689), (1436, 1779), 'text', 'debut_prise_en_charge']]

    ################################# traitement et extraction des informations ###################"
    eIOf = extracInformationOfformula(roi, pixelsTreshold)
    IMG_DIRECTORY = '/Users/jeanmichelcheumeni/Desktop/CV_Maif/data/form/'
    saveNameFile = "/Users/jeanmichelcheumeni/Desktop/CV_Maif/scriptForms/dataForm.csv"
    ## appel des différentes methode de la class définie ci-dessus
    for name in os.listdir(IMG_DIRECTORY)[:1]:
        images = cv2.imread(IMG_DIRECTORY + name)
        data, imgShow = eIOf.analyseImages(images)
        eIOf.saveDataForCsv(saveNameFile, data)

        print(data)
        cv2.imshow('img', imgShow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
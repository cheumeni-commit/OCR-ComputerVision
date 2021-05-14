# Computer Vision
# Extraction d'information sur des images
# Author : JM Cheumeni
import cv2
import numpy as np
import os
import time
import configparser as cfg
import traceback
import pytesseract
from pytesseract import *
#from pyzbar import pyzbar

from tableData import roi, nameImage


class ObjectExtractor():

    # Initialisation des variables du .ini
    def __init__(self, configFile, configSection = 'DEFAULT'):

        self.roi = roi
        self._loadConfig(configFile, configSection)

    def _loadConfig(self, configFile, configSection):
        config = cfg.ConfigParser()
        config.read(configFile)
        try:
            self.traceInfo = config.getboolean(configSection, 'traceInfo')
            self.detectionThreshold = config.getfloat(configSection, 'detectionThreshold')
            imageSizeStr = config.get(configSection, 'imageSize')
            self.imageSize = (int(imageSizeStr.split(',')[0]),
                              int(imageSizeStr.split(',')[1]), int(imageSizeStr.split(',')[2]))
        except Exception as e:
            if not os.path.isfile(configFile):
                print('No such config file : ' + configFile)
                print(str(e))
                print(traceback.format_exc())
                raise SystemExit('No such config file : ' + configFile)
            else:
                print('Problem loading configuration file : ' + configFile)
                print(str(e))
                print(traceback.format_exc())
                raise SystemExit('Problem loading configuration file : ' + configFile)

    def remove_noise(self,image):
        '''
        :param image: image bruitée
        :return: image non bruitée
        '''
        return cv2.medianBlur(image, 1)

    def extractBoxLetterinformation(self, imroot, MyData):

            imgCrop = None
            for name in nameImage:
                img = cv2.imread(imroot + name)
                print(name)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = self.remove_noise(img)
                hImg, wImg = img.shape
                imgCrop = img[200:, :]

                boxes = pytesseract.image_to_string(imgCrop, lang='fra')
                print(list(set(boxes.strip().split('\n'))))
                MyData[name].append(list(set(boxes.strip().split('\n'))))
                cv2.imshow('img', imgCrop)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

    def extractionBoxOfImage(self, imroot, MyData):

        img = None
        for name in nameImage:
            img = cv2.imread(imroot + name)
            print(name)
            img = cv2.pyrDown(self.remove_noise(img))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Performing OTSU threshold
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
            grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, rect_kernel)

            ret, thresh1 = cv2.threshold(grad, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
            connected = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)

            contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            mask = np.zeros(thresh1.shape, dtype=np.uint8)

            for idx in range(len(contours)):

                x, y, w, h = cv2.boundingRect(contours[idx])
                mask[y:y + h, x:x + w] = 0
                cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)

                r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)
                if r > 0.4 and w > 2 and h > 2:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Cropping the text block for giving input to OCR
                    cropped = img[y:y + h , x:x + w ]
                    text = pytesseract.image_to_string(cropped, lang='fra')
                    #print(text.strip().split('\n'))
                    if text.strip().split('\n')[0] != '':
                        MyData[name].append(text.strip().split('\n')[0])
                        print(MyData)

            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    def extractionBoxWordInformation(self, imroot, MyData):

        '''
        :param imroot:
        :param MyData:
        :return:
        '''

        img = None
        for name in nameImage:
            img = cv2.imread(imroot + name)
            print(name)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = self.remove_noise(img)
            hImg, wImg, _ = img.shape

            boxes = pytesseract.image_to_data(img, lang='fra')
            #print(boxes)
            for ite, box in enumerate(boxes.splitlines()):
                if ite != 0:
                    box = box.split()
                    #print(box)
                    if len(box) == 12:
                        x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                        cv2.rectangle(img, (x, y), (w+x, y+h), (0, 0, 255), 1)
                        MyData[name].append(box[11])
                        print(MyData)

            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    def extractionQRcode(self, image):
         '''

         :param image:
         :return:
         '''

    def analyseImages(self, imroot, MyData):
        '''

        :param images: traitemet des images
        :return: donnees extraites et l'image avec le mask
        '''
        #data = {a:[] for a in nameImage}
        imgShow = None
        for i in range(len(nameImage)):
            for j in range(len(self.roi)):
                if nameImage[i] == self.roi[j][0]:
                    images = cv2.imread(imroot + nameImage[i])
                    imgShow = images.copy()
                    imgMask = np.zeros_like(imgShow)

                    cv2.rectangle(imgMask, (self.roi[j][1][0], self.roi[j][1][1]), (self.roi[j][2][0], self.roi[j][2][1]), (0,255,0), cv2.FILLED)
                    imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 2, 0)
                    # cropping des region d'interet : ROI
                    imgCrop = images[self.roi[j][1][1]:self.roi[j][2][1], self.roi[j][1][0]:self.roi[j][2][0]]
                    imgCrop = self.remove_noise(imgCrop)
                    ## binarisation de l'image croppee
                    imgCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
                    cv2.imshow(str(j), imgCrop)
                    if cv2.waitKey(1) & 0xff == ord('q'):
                        break

                    if self.roi[j][3] == 'text':
                         print(f'{self.roi[j][4]} : {pytesseract.image_to_string(imgCrop)}')
                         if nameImage[i] in MyData:
                            MyData[nameImage[i]].append(pytesseract.image_to_string(imgCrop, lang='fra').strip())
                            print(MyData)
                         else:
                            MyData[nameImage[i]].append(pytesseract.image_to_string(imgCrop, lang='fra').strip())

    def saveDataForCsv(self, nameFile, data):
        '''

        :param nameFile: fichier de sortie des donnees (.csv)
        :param data: donnees a stocker dans le fichier
        :return:
        '''
        with open(nameFile, 'a') as f:
            for name in nameImage:
                f.write((str(name) + ';'))
                for i in range(len(data[name])):
                    if i < len(data[name])-1:
                        f.write((str(data[name][i])+';'))
                    else:
                        f.write(str(data[name][i]))
                f.write('\n')

if __name__ == "__main__":

    imroot = '/Users/jeanmichelcheumeni/Desktop/CV_Maif/data/poster/'
    saveNameFile = "/Users/jeanmichelcheumeni/Desktop/CV_Maif/scriptPoster/resultatsExtractionInfo.csv"
    MyData = {a: [] for a in nameImage}

    ObjExt = ObjectExtractor('/Users/jeanmichelcheumeni/Desktop/CV_Maif/scriptPoster/ObjectExtractor.ini' , 'DEFAULT')
    ## extraction information importantes sur l'image
    ObjExt.analyseImages(imroot, MyData)
    #ObjExt.extractBoxLetterinformation(imroot, MyData)
    #ObjExt.extractionBoxOfImage(imroot, MyData)
    #ObjExt.extractionBoxWordInformation(imroot, MyData)

    ## sauvegarde des informations dans un fichier .csv
    ObjExt.saveDataForCsv(saveNameFile, MyData)









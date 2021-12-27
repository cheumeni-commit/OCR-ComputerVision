import cv2
import numpy as np
import pytesseract

from src.constants import (c_PIXEL_THRESHOLD,
                           c_ROI
                           )


def analyseImages(images):
    '''
    :param images: traitement des images
    :return: donnees extraites et l'image avec le mask
    '''
    imgShow = images.copy()
    imgMask = np.zeros_like(imgShow)
    data = []

    for _, r in enumerate(c_ROI):

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
            if totalPixels > c_PIXEL_THRESHOLD :
                totalPixels = "oui"
            else:
                totalPixels = "non"
            print(f'{r[3]} : {totalPixels}')
            data.append(totalPixels.strip())

    return data, imgShow



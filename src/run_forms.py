import os

import cv2

from src.constants import (c_DATA_FORME)
from src.config.directories import directories as dirs
from src.scriptForms.extractFormulaInformation import analyseImages
from src.io import saveDataForCsv


def main():
    for name in os.listdir(dirs.dir_form)[:1]:
        images = cv2.imread(dirs.dir_form + name)
        data, imgShow = analyseImages(images)
        saveDataForCsv(data, path=dirs.dir_src_dataIn / c_DATA_FORME)
        #
        print(data)
        cv2.imshow('img', imgShow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()
import cv2
from time import sleep
import os
import numpy as np
import datetime


def fromF():
    path = "r:\\z1"
    arr = os.listdir(path)
    img = []
    if len(arr) > 15:
        print(arr[1])
        file = path + "\\" + arr[1]
        img = cv2.imread(file)
        os.remove(file)
    return img


if __name__ == '__main__':
    key = 0
    while key != 27:
        img = fromF()
        if img != []:
            # img = cv2.resize(img, (960, 540))
            # img = cv2.resize(img, (640, 360))
            cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF
    # cv2.destroyAllWindows()

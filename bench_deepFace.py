from deepface import DeepFace
import cv2

import time

if __name__ == '__main__':
    img1 = cv2.imread('10.jpg')
    img2 = cv2.imread('10.jpg')
    for i in range(10):
        start_time = time.time()
        output = DeepFace.verify(img1, img2)
        print(output)
        print(time.time() - start_time, " \n")
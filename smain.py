from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import time

def verify(img1, img2):
    # plt.imshow(img1[:, :, ::-1])
    # plt.show()
    # plt.imshow(img2[:, :, ::-1])
    # plt.show()
    output = DeepFace.verify(img1, img2, model_name='SFace')
    print(output)
    verification = output['verified']
    # if verification:
    #     print('They are same')
    # else:
    #     print('The are not same')


if __name__ == '__main__':
    img1 = cv2.imread('3.jpg')
    img2 = cv2.imread('4.jpg')
    for i in range(1000):
        start_time = time.time()
        verify(img1, img2)
        print(time.time() - start_time, " \n")
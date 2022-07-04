import cv2
import numpy as np
from deepface import DeepFace
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def face_detect():
    image1 = request.form['image1']
    image2 = request.form['image2']

    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    scale = 40
    h1, w1 = int(img1.shape[0] * (scale / 100)), int(img1.shape[1] * (scale / 100))
    h2, w2 = int(img2.shape[0] * (scale / 100)), int(img2.shape[1] * (scale / 100))

    img1 = cv2.resize(img1, (w1, h1), interpolation=cv2.INTER_NEAREST)
    img2 = cv2.resize(img2, (w2, h2), interpolation=cv2.INTER_NEAREST)

    verification = DeepFace.verify(img1_path=img1, img2_path=img2,
                                   model_name='SFace', distance_metric='euclidean_l2',
                                   detector_backend='opencv')
    # VGG-Face, Facenet, OpenFace, DeepFace, DeepID, Dlib, ArcFace or Ensemble

    return str(verification['verified'])


if __name__ == '__main__':
    app.run()
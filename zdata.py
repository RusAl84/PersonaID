import json
import os
from PIL import Image
from deepface import DeepFace
import numpy as np
import pickle
import face_recognition

def load(filename="./photo/zdata.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        jsonstring = file.read()
    zdata = []
    zdata = json.loads(jsonstring)
    return zdata

def loadEmb():
    with open('known_encodings.pickle', 'rb') as handle:
        known_encodings = pickle.load(handle)
    with open('known_images.pickle', 'rb') as handle:
        known_images = pickle.load(handle)
    with open('known_names.pickle', 'rb') as handle:
        known_names = pickle.load(handle)
    return (known_encodings, known_images, known_names)

def saveEmb2():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    known_images = []
    known_encodings = []
    known_names = []
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "Dlib", "ArcFace"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    for item in zdata:
        image = Image.open(path + item['filename'])
        known_names.append(item['name'])
        known_images.append(image)
        img = np.asarray(image)
        face_encoding = DeepFace.represent(img, model_name=models[5],
                                           enforce_detection=False, detector_backend=backends[5])
        known_encodings.append(face_encoding / np.linalg.norm(face_encoding))
    with open('known_encodings.pickle', 'wb') as handle:
        pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_images.pickle', 'wb') as handle:
        pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_names.pickle', 'wb') as handle:
        pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

def saveEmb():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    known_images = []
    known_encodings = []
    known_names = []
    for item in zdata:
        image = face_recognition.load_image_file(path + item['filename'])
        known_images.append(image)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(face_encoding)
        # known_names.append(item['name'])
    with open('known_encodings.pickle', 'wb') as handle:
        pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_images.pickle', 'wb') as handle:
        pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_names.pickle', 'wb') as handle:
        pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    zdata = load()
    for item in zdata:
        print(f"{item['filename']} {item['name']} {item['desc']}")
    saveEmb()

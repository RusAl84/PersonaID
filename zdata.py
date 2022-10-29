import json
import os
from PIL import Image
# from deepface import DeepFace
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
        # face_encoding = DeepFace.represent(img, model_name=models[1],
        #                                    enforce_detection=False, detector_backend=backends[5])
        # known_encodings.append(face_encoding / np.linalg.norm(face_encoding))
    with open('known_encodings.pickle', 'wb') as handle:
        pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_images.pickle', 'wb') as handle:
        pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_names.pickle', 'wb') as handle:
        pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)


def saveEmb():
    zdata = load()
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    known_images = []
    known_encodings = []
    known_names = []
    emb_crc = {}
    if os.path.exists("emb_crc.pickle"):
        with open('emb_crc.pickle', 'rb') as handle:
            emb_crc = pickle.load(handle)
    for item in zdata:
        known_names.append(item['name'])
        datafile = path + item['filename']
        print(datafile)
        image = face_recognition.load_image_file(datafile)
        known_images.append(image)
        if os.path.exists(datafile + ".pickle"):
            if datafile in emb_crc:
                if os.path.getsize(datafile) != emb_crc[datafile]:
                    face_encoding = face_recognition.face_encodings(image)[0]
                    known_encodings.append(face_encoding)
                    with open(datafile + '.pickle', 'wb') as handle:
                        pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    emb_crc[datafile] = os.path.getsize(datafile)
                else:
                    with open(datafile + '.pickle', 'rb') as handle:
                        face_encoding = pickle.load(handle)
                    known_encodings.append(face_encoding)
            else:
                face_encoding = face_recognition.face_encodings(image)[0]
                known_encodings.append(face_encoding)
                with open(datafile + '.pickle', 'wb') as handle:
                    pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
                emb_crc[datafile] = os.path.getsize(datafile)
        else:
            face_encoding = face_recognition.face_encodings(image)[0]
            known_encodings.append(face_encoding)
            with open(datafile + '.pickle', 'wb') as handle:
                pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
            emb_crc[datafile] = os.path.getsize(datafile)
    with open('known_encodings.pickle', 'wb') as handle:
        pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_images.pickle', 'wb') as handle:
        pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('known_names.pickle', 'wb') as handle:
        pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('emb_crc.pickle', 'wb') as handle:
        pickle.dump(emb_crc, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def addUser():
#     path = "\\\\desktop-rk6qjih\\Users\\Dell7\\Desktop\\FaceRecog\\photo\\zdata.json"


def genData():
    zdata = load()
    # num = 0
    # for item in zdata:
    #     print(f"{num} {item['filename']} {item['name']} {item['desc']}")
    #     num += 1
    # saveEmb()
    # print("embeddings is generated")
    lines = []
    with open("./new/data.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    dicRecord = dict()
    dicRecord["filename"] = "\\photo\\" + lines[0].replace("\n", "")
    dicRecord["name"] = lines[1].replace("\n", "")
    dicRecord["desc"] = lines[2].replace("\n", "")
    zdata.append(dicRecord)
    jsonstring = json.dumps(zdata)
    jsonstring = jsonstring.replace("\\/", "/").encode().decode('unicode_escape')
    jsonstring = jsonstring.replace("\\", "\\\\")
    # print(jsonstring)
    with open("./new/zdata.json", 'w', encoding='utf-8') as file:
        file.write(jsonstring.encode().decode("UTF-8"))


def getDBsize():
    filename = "./photo/zdata.json"
    if os.path.exists(filename):
        return os.path.getsize(filename)


def isChange():
    filename = "./photo/zdata.json"
    if os.path.exists(filename):
        return os.path.getsize(filename)


if __name__ == '__main__':
    zdata = load()
    # num = 0
    # for item in zdata:
    #     print(f"{num} {item['filename']} {item['name']} {item['desc']}")
    #     num += 1
    saveEmb()
    # print("embeddings is generated")

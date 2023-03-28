import json
import os
import time
from PIL import Image
# from deepface import DeepFace
import numpy as np
import pickle
import face_recognition
import psycopg2
import json
from json import JSONEncoder
import numpy
import shutil


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                              database="personadb")

photopath = ".\\photo\\"
newpath = ".\\new\\"

# def load(filename="./photo/zdata.json"):
#     with open(filename, 'r', encoding='utf-8') as file:
#         jsonstring = file.read()
#     zdata = []
#     zdata = json.loads(jsonstring)
#     return zdata


# def loadEmb():
#     with open('known_encodings.pickle', 'rb') as handle:
#         known_encodings = pickle.load(handle)
#     # with open('known_images.pickle', 'rb') as handle:
#     #     known_images = pickle.load(handle)
#     # with open('known_names.pickle', 'rb') as handle:
#     #     known_names = pickle.load(handle)
#     return known_encodings


# def saveEmb2():
#     full_path = os.path.realpath(__file__)
#     path, filename = os.path.split(full_path)
#     known_images = []
#     known_encodings = []
#     known_names = []
#     models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "Dlib", "ArcFace"]
#     backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
#     for item in zdata:
#         image = Image.open(path + item['filename'])
#         known_names.append(item['name'])
#         known_images.append(image)
#         img = np.asarray(image)
#         # face_encoding = DeepFace.represent(img, model_name=models[1],
#         #                                    enforce_detection=False, detector_backend=backends[5])
#         # known_encodings.append(face_encoding / np.linalg.norm(face_encoding))
#     with open('known_encodings.pickle', 'wb') as handle:
#         pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     with open('known_images.pickle', 'wb') as handle:
#         pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     with open('known_names.pickle', 'wb') as handle:
#         pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def saveEmb():
#     zdata = load()
#     full_path = os.path.realpath(__file__)
#     path, filename = os.path.split(full_path)
#     # known_images = []
#     known_encodings = []
#     # known_names = []
#     # emb_crc = {}
#     # if os.path.exists("emb_crc.pickle"):
#     #     with open('emb_crc.pickle', 'rb') as handle:
#     #         emb_crc = pickle.load(handle)
#     for item in zdata:
#         # known_names.append(item['name'])
#         datafile = path + item['filename']
#         print(datafile)
#         image = face_recognition.load_image_file(datafile)
#         # known_images.append(image)
#         if os.path.exists(datafile + ".pickle"):
#             if datafile in emb_crc:
#                 if os.path.getsize(datafile) != emb_crc[datafile]:
#                     face_encoding = face_recognition.face_encodings(image)[0]
#                     known_encodings.append(face_encoding)
#                     with open(datafile + '.pickle', 'wb') as handle:
#                         pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
#                     emb_crc[datafile] = os.path.getsize(datafile)
#                 else:
#                     with open(datafile + '.pickle', 'rb') as handle:
#                         face_encoding = pickle.load(handle)
#                     known_encodings.append(face_encoding)
#             else:
#                 face_encoding = face_recognition.face_encodings(image)[0]
#                 known_encodings.append(face_encoding)
#                 with open(datafile + '.pickle', 'wb') as handle:
#                     pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
#                 emb_crc[datafile] = os.path.getsize(datafile)
#         else:
#             face_encoding = face_recognition.face_encodings(image)[0]
#             known_encodings.append(face_encoding)
#             with open(datafile + '.pickle', 'wb') as handle:
#                 pickle.dump(face_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)
#             # emb_crc[datafile] = os.path.getsize(datafile)
#     with open('known_encodings.pickle', 'wb') as handle:
#         pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     # with open('known_images.pickle', 'wb') as handle:
#     #     pickle.dump(known_images, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     # with open('known_names.pickle', 'wb') as handle:
#     #     pickle.dump(known_names, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     # with open('emb_crc.pickle', 'wb') as handle:
#     #     pickle.dump(emb_crc, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def saveEmb2():
#     zdata = load()
#     full_path = os.path.realpath(__file__)
#     path, filename = os.path.split(full_path)
#
#     known_encodings = []
#     for item in zdata:
#         # known_names.append(item['name'])
#         datafile = path + item['filename']
#         print(datafile)
#         image = face_recognition.load_image_file(datafile)
#         face_encoding = face_recognition.face_encodings(image)[0]
#         known_encodings.append(face_encoding)
#     with open('known_encodings.pickle', 'wb') as handle:
#         pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)

# def saveEmb3():
#     zdata = load()
#     full_path = os.path.realpath(__file__)
#     path, filename = os.path.split(full_path)
#
#     known_encodings = []
#     for item in zdata:
#         # known_names.append(item['name'])
#         datafile = path + item['filename']
#         print(datafile)
#         image = face_recognition.load_image_file(datafile)
#         face_encoding = face_recognition.face_encodings(image)[0]
        # insertDB
    #     known_encodings.append(face_encoding)
    # with open('known_encodings.pickle', 'wb') as handle:
    #     pickle.dump(known_encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)

# def addUser():
#     path = "\\\\desktop-rk6qjih\\Users\\Dell7\\Desktop\\FaceRecog\\photo\\zdata.json"


# def genData():
#     zdata = load()
#     # num = 0
#     # for item in zdata:
#     #     print(f"{num} {item['filename']} {item['name']} {item['desc']}")
#     #     num += 1
#     # saveEmb()
#     # print("embeddings is generated")
#     lines = []
#     with open("./new/data.txt", 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#     dicRecord = dict()
#     dicRecord["filename"] = "\\photo\\" + lines[0].replace("\n", "")
#     dicRecord["name"] = lines[1].replace("\n", "")
#     dicRecord["desc"] = lines[2].replace("\n", "")
#     zdata.append(dicRecord)
#     jsonstring = json.dumps(zdata)
#     jsonstring = jsonstring.replace("\\/", "/").encode().decode('unicode_escape')
#     jsonstring = jsonstring.replace("\\", "\\\\")
#     # print(jsonstring)
#     with open("./new/zdata.json", 'w', encoding='utf-8') as file:
#         file.write(jsonstring.encode().decode("UTF-8"))


# def getDBsize():
#     filename = "./photo/zdata.json"
#     if os.path.exists(filename):
#         return os.path.getsize(filename)
#
#
# def isChange():
#     filename = "./photo/zdata.json"
#     if os.path.exists(filename):
#         return os.path.getsize(filename)

def DB_Clear():
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    connection.autocommit = True
    cursor = connection.cursor()
    sql_delete_query = 'Delete from public.zemb'
    cursor.execute(sql_delete_query)
    connection.commit()
    time.sleep(0.01)
    photopath = ".\\photo\\"
    filelist = [f for f in os.listdir(photopath)]
    for f in filelist:
        os.remove(os.path.join(photopath, f))

def isExist(filename):
    cursor = connection.cursor()
    postgreSQL_select_Query = f"SELECT filename FROM public.zemb WHERE filename='{str(filename)}' ORDER BY id DESC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        if filename == datarecord[0]:
            return True
        else:
            return False
    else:
        return False


def addEmb():
    connection.autocommit = True
    filelist = [f for f in os.listdir(newpath)]
    num=0
    for f in filelist:
        # print(os.path.join(photopath, f))
        filename=f"{os.path.join(newpath, f)}\\data.txt"
        lines=[]
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if len(lines)>0:
            name = str(lines[0]).replace("\n","")
            desc = str(lines[1]).replace("\n","")
            filename = str(lines[2]).replace("\n","")
            if not isExist(filename):
                cursor = connection.cursor()
                sql_insert_with_param = """INSERT INTO public.zemb
                                      (emb, filename, name, "desc", sound)
                                      VALUES (%s, %s, %s, %s, %s);"""
                os.replace(f"{newpath}{f}\\{filename}", f"{photopath}{filename}")
                sound = ""
                image = face_recognition.load_image_file(f"{photopath}{filename}")
                face_encoding = face_recognition.face_encodings(image)[0]
                encodedNumpyData = json.dumps(face_encoding, cls=NumpyArrayEncoder)  # use dump() to write array into file
                # print("Printing JSON serialized NumPy array")
                # print(encodedNumpyData)
                emb = str(encodedNumpyData)
                if len(lines)==4:
                    sound = str(lines[3]).replace("\n","")
                    os.replace(f"{newpath}{f}\\{sound}", f"{photopath}{sound}")
                data_tuple = (emb, filename, name, desc, sound)
                cursor.execute(sql_insert_with_param, data_tuple)
                connection.commit()
                print(f"Emb added: {name}")
                shutil.rmtree(f"{newpath}{f}")
                num+=1
            else:
                shutil.rmtree(f"{newpath}{f}")
    return num

def getEmb():
    lines=[]
    cursor = connection.cursor()
    postgreSQL_select_Query = """SELECT id, emb, filename, "name", "desc", sound FROM public.zemb ORDER BY id ASC"""
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchall()
    if datarecord:
        for item in datarecord:
            line = {}
            line['id']=item[0]
            decodedArrays = json.loads(item[1])
            finalNumpyArray = numpy.array(decodedArrays)
            # print("NumPy Array")
            # print(finalNumpyArray)
            line["emb"]=finalNumpyArray
            line["filename"]=item[2]
            line["name"]=item[3]
            line["desc"]=item[4]
            line["sound"]=item[5]
            lines.append(line)
    return lines

def checkNew():
    if len(os.listdir('/your/path')) == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    # DB_Clear()
    # addEmb()
    emb = getEmb()
    print(emb[0])



# # Deserialization
# print("Decode JSON serialized NumPy array")
# decodedArrays = json.loads(encodedNumpyData)
#
# finalNumpyArray = numpy.asarray(decodedArrays["array"])
# print("NumPy Array")
# print(finalNumpyArray)
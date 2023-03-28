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
connection.autocommit = True

photopath = ".\\photo\\"
newpath = ".\\new\\"

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
    if len(os.listdir(newpath)) == 0:
        return False
    else:
        return True

def getDataById(emb, id):
    for item in emb:
        if item['id']==id:
            return item

if __name__ == '__main__':
    # DB_Clear()
    # addEmb()
    # emb = getEmb()
    # print(emb[0])
    print(checkNew())



# # Deserialization
# print("Decode JSON serialized NumPy array")
# decodedArrays = json.loads(encodedNumpyData)
#
# finalNumpyArray = numpy.asarray(decodedArrays["array"])
# print("NumPy Array")
# print(finalNumpyArray)
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
import time
import datetime


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
delpath = ".\\del\\"
default_path = ".\\default\\"
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
                milliseconds = int(time.time() * 1000)
                dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
                dt = str(dt).replace(':','_')
                shutil.copytree(f"{newpath}{f}", f"{delpath}{str(f+'_'+dt)}")
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
                #shutil.move(src, dst, copy_function=copy2) - рекурсивно перемещает файл или директорию (src) в другое место (dst), и возвращает место назначения.
                # shutil.move(f"{newpath}{f}", f"{delpath}{str(f+str(dt))}", copy_function=copy2)
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

def isChanged(count):
    cursor = connection.cursor()
    postgreSQL_select_Query = """SELECT id FROM public.zemb ORDER BY id ASC"""
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchall()
    if len(datarecord)==count:
        return False
    else:
        return True

def getDataById(emb, id):
    for item in emb:
        if item['id']==id:
            return item


def copy_folders_with_depth(src_dir, dst_dir, max_depth=1):
    """
    Копирует папки с ограничением глубины вложенности
    """
    os.makedirs(dst_dir, exist_ok=True)
    
    def copy_recursive(src, dst, current_depth):
        if current_depth > max_depth:
            return
            
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            
            if os.path.isdir(src_path):
                try:
                    shutil.copytree(src_path, dst_path)
                    print(f"Скопирована (глубина {current_depth}): {item}")
                except FileExistsError:
                    print(f"Пропущена (существует): {item}")
                
                # Рекурсивно копируем вложенные папки
                copy_recursive(src_path, dst_path, current_depth + 1)
    
    copy_recursive(src_dir, dst_dir, 1)


if __name__ == '__main__':
    DB_Clear()
    # Копировать только папки первого уровня
    copy_folders_with_depth(default_path, newpath, max_depth=1)
    addEmb()
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
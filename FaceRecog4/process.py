import datetime
import json
import os

import cv2
import psycopg2
import time
import numpy as np
import simplejpeg
import face_recognition

def toPG(connection, img):
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    # _, data = cv2.imencode('.jpg', img, encode_param)
    # frame = data.tobytes()
    frame = simplejpeg.encode_jpeg(image=img, quality=90)
    milliseconds = int(time.time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # print(dt)
    score = milliseconds
    cursor = connection.cursor()
    sql_insert_with_param = """INSERT INTO z2frame
                          (frame, milliseconds ,timestr)
                          VALUES (%s, %s, %s);"""
    data_tuple = (frame, milliseconds, dt)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()
    return


def fromPG(connection):
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM public.z1frame ORDER BY milliseconds DESC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        bbox = datarecord[4]
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        print(bbox)
        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        # img = bytearray(frame)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img, bbox


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    with open("./photo/zdata.json", 'r', encoding='utf-8') as file:
        jsonstring = file.read()
    zdata = json.loads(jsonstring)
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    faces_info = {}
    known_images = []
    known_encodings = []
    known_names = []
    for item in zdata:
        image = face_recognition.load_image_file(path + item['filename'])
        known_images.append(image)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(face_encoding)
        known_names.append(item['name'])
    max_face_distance
    # cursor = connection.cursor()
    # sql_delete_query = "Delete from public.z1frame"
    # cursor.execute(sql_delete_query)
    # connection.commit()
    # time.sleep(0.5)
    while True:
        frame, bbox = fromPG(connection)
        # frame = cv2.resize(frame, (495, 270))
        if len(frame) > 1:
            # toPG(connection, frame)
            time.sleep(0.01)

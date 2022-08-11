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
    bboxs = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        bboxs = datarecord[4]
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        if len(bboxs)>2:
            bboxs = json.loads(bboxs)
        print(bboxs)

        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        # img = bytearray(frame)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return (img, bboxs)


def recognize(bboxs, frame, known_encodings, max_face_distance):
    face_locations = [(bbox[1][1], bbox[1][0] + bbox[1][2], bbox[1][1] + bbox[1][3], bbox[1][0]) for bbox in bboxs]
    rgb_frame = frame[:, :, ::-1]
    face_names = []
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index] and min(face_distances) < max_face_distance:
            name = known_names[best_match_index]
            print(name, face_distances)

        face_names.append(name)

    for i in range(len(face_names)):
        if face_names[i] != "Unknown":
            faces_info[face_names[i]] = (bboxs[i], time.time())

    return face_names


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
    max_face_distance = 0.55
    # cursor = connection.cursor()
    # sql_delete_query = "Delete from public.z1frame"
    # cursor.execute(sql_delete_query)
    # connection.commit()
    # time.sleep(0.5)
    while True:
        frame, bboxs = fromPG(connection)
        # frame = cv2.resize(frame, (495, 270))
        if len(frame) > 1 and len(bboxs) > 2:
            face_names = recognize(bboxs, frame, known_encodings, max_face_distance)
            # toPG(connection, frame)
            print(face_names)

            time.sleep(0.01)

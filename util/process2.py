import datetime
import io
import json
import os
import random
import cv2
import psycopg2
import time
import numpy as np
import simplejpeg
import zdata as zd
from PIL import Image
from deepface import DeepFace


def toPG(connection, nboxs, milliseconds):
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    # _, data = cv2.imencode('.jpg', img, encode_param)
    # frame = data.tobytes()
    # frame = simplejpeg.encode_jpeg(image=img, quality=90)
    # milliseconds = int(time.time() * 1000)
    zjson = json.dumps(str(nboxs))
    milliseconds = int(milliseconds)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # # print(dt)
    # score = milliseconds
    cursor = connection.cursor()
    sql_insert_with_param = """INSERT INTO zdata
                          (zjson, milliseconds ,timestr)
                          VALUES (%s, %s, %s);"""
    data_tuple = (zjson, milliseconds, dt)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()
    return


def toPGzdash(connection, milliseconds, timestr, photo, name, capture, name_id):
    # # print(dt)
    # score = milliseconds
    cursor = connection.cursor()
    sql_insert_with_param = """INSERT INTO public.zdash
                          (milliseconds, timestr, photo, name, capture, name_id)
                          VALUES (%s, %s, %s, %s, %s, %s);"""
    data_tuple = (milliseconds, timestr, photo, name, capture, name_id)
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
    milliseconds = 0
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        bboxs = datarecord[4]
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        bboxs = bboxs.replace("'", "")
        bboxs = bboxs.replace("\"", "")
        import ast
        bboxs = ast.literal_eval(bboxs)
        # bboxs= json.loads(bboxs)
        # print(bboxs[0])

        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        # img = bytearray(frame)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img, bboxs, milliseconds


def compare(embeddings, embedding2):
    similar_faces = dict()
    for i in range(len(embeddings)):
        diff = np.subtract(embeddings[i], embedding2)
        dist = np.sum(np.square(diff), 0)
        similar_faces[i] = dist
    return similar_faces


def recognize(bboxs, frame, known_encodings, max_face_distance, zdata):
    ## face_location = (minY, minX+maxX, minY+maxY, minX)
    # face_locations = [(bbox[1][1], bbox[1][0] + bbox[1][2], bbox[1][1] + bbox[1][3], bbox[1][0]) for bbox in bboxs]

    ## face_location = (minY, maxY, minX, maxX)
    face_locations = [(bbox[1][0], bbox[1][1], bbox[1][2], bbox[1][3]) for bbox in bboxs]

    rgb_frame = frame[:, :, ::-1]

    face_encodings = []
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "Dlib", "ArcFace"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

    face_names = []
    for box in face_locations:
        # cv2.imshow("frame", frame)
        # cv2.imwrite("./frame.png", frame)
        x, y, w, h = box
        cropped = frame[y:y + h, x:x + w]
        # cv2.imwrite("./cropped.png", cropped)
        tEMB = DeepFace.represent(cropped, model_name=models[1],
                                                 enforce_detection=False, detector_backend=backends[5])
        tEMB = tEMB/np.linalg.norm(tEMB)
        face_encodings.append(tEMB)
        # cv2.imshow("cropped", cropped)
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = compare(known_encodings, face_encoding)
        print(matches)
        # use the known face with the smallest distance to the new face
        best_match_index = min(matches, key=matches.get)
        treshold = 0.7
        if len(matches) != -1 and matches[best_match_index] < treshold:
            name = best_match_index
            print(matches[best_match_index])
            # print(name, face_distances)
        else:
            name = -1
        face_names.append(name)
    nbboxs = []
    for i in range(len(bboxs)):
        item = bboxs[i]
        item.append(face_names[i])
        if face_names[i] != -1:
            nbboxs.append(item)
    return nbboxs


def get_lifetime(connection, face_id):
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT milliseconds FROM public.zdash WHERE name_id=" + str(
        face_id) + " ORDER BY milliseconds DESC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        mill = datarecord[0]
        return mill
        # milliseconds = int(time.time() * 1000)
        # return milliseconds - mill
    else:
        return -1


def is_first_dash(connection):
    cursor = connection.cursor()
    postgreSQL_select_Query = "select count(*) from public.zdash"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        count = datarecord[0]
        return count == 0
    else:
        return -1


def get_dash_last_faceid(connection):
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT name_id FROM public.zdash ORDER BY id DESC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        face_id = datarecord[0]
        return face_id
    else:
        return -1


def fasceID_exist(face_id, connection):
    cursor = connection.cursor()
    postgreSQL_select_Query = f"SELECT count(*) FROM public.zdash WHERE name_id={face_id}"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        count = datarecord[0]
        if count > 0:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    zdata = zd.load()
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    known_images = []
    known_encodings = []
    known_names = []

    ## TODO: Сделать проверку новых картинок
    (known_encodings, known_images, known_names) = zd.loadEmb()

    max_face_distance = 1
    life_time = 60 * 1000
    t_life_time = 0

    while True:
        # for i in range(10):
        frame, bboxs, milliseconds = fromPG(connection)
        # frame = cv2.resize(frame, (495, 270))
        if len(frame) > 1:
            nboxs = recognize(bboxs, frame, known_encodings, max_face_distance, zdata)
            if len(nboxs) > 0:
                toPG(connection, nboxs, milliseconds)
                # cv2.imwrite("2.jpg", frame)
                for bitem in nboxs:
                    face_id = bitem[3]
                    # c_life_time = int(time.time() * 1000)
                    # t_life_time = get_lifetime(connection, face_id)
                    # is_fdash = is_first_dash(connection)
                    # c_face_id = get_dash_last_faceid(connection)
                    # print(f"{c_life_time} {t_life_time} {abs(t_life_time - c_life_time)}   ")
                    # if (abs(t_life_time - c_life_time) > life_time and t_life_time > 0) \
                    #         or is_fdash \
                    #         or (c_face_id > 0 and c_face_id != face_id):
                    face_id_exist = fasceID_exist(face_id, connection)
                    # face_id_exist = False
                    if not face_id_exist:
                        bboxs = bitem[1]
                        img = simplejpeg.encode_jpeg(image=frame, quality=90)
                        im = Image.open(io.BytesIO(img))
                        width, height = im.size
                        padding = 20
                        x1 = bboxs[0] - padding
                        y1 = bboxs[1] - padding
                        x2 = bboxs[0] + bboxs[2] + padding
                        y2 = bboxs[1] + bboxs[3] + padding
                        if x1 < 0:
                            x1 = 0
                        if y1 < 0:
                            y1 = 0
                        if x2 > width:
                            x2 = width
                        if y2 > height:
                            y2 = height
                        pixels = (x1, y1, x2, y2)
                        fname_str = ".\\capture\\" + str(milliseconds) + "_" + str(random.randint(0, 10 ** 10)) + ".jpg"
                        im_crop = im.crop(pixels)
                        im_crop.save(fname_str, quality=80)
                        print(bitem, zdata[face_id]['name'], face_id, milliseconds)
                        capture = fname_str.replace('.', '')
                        capture = capture.replace('\\', '/')
                        capture = capture.replace('jpg', '.jpg')
                        name = str(zdata[face_id]['name'])
                        name_id = str(face_id)
                        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
                        timestr = str(dt)
                        photo = str(zdata[face_id]['filename'])
                        photo = photo.replace('\\', '/')
                        url = "http://127.0.0.1:5000"
                        toPGzdash(connection, str(milliseconds), timestr, url + photo, name, url + capture, name_id)
            time.sleep(0.01)

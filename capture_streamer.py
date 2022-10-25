import datetime
import json
import pyvirtualcam
from pyvirtualcam import PixelFormat
import numpy as np
import cv2
import psycopg2
import time
import os
import simplejpeg
import mediapipe as mp
import zdata as zd
import random


def DrawFPS(img, fps):
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)


def findFaces(img, faceDetection):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    # print(self.results)
    bboxs = []
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            bboxs.append([id, bbox, detection.score])
    return img, bboxs


def DrawRectagle(img, bbox, gbboxs, detection_score, l=30, t=5, rt=3, dpix=80):
    for box in bbox:
        num = box[0]
        dots = box[1]
        score = box[2][0]
        # text =  box[2]
        newgbboxs = gbboxs
        if score >= detection_score:
            x, y, w, h = dots
            x1, y1 = x + w, y + h
            color = (0, 255, 0)
            cv2.rectangle(img, dots, color, rt)
            cMilliseconds = int(time.time() * 1000)
            newgbboxs = []
            num = -1
            d = 10 ** 8
            name = ""
            for gitem in gbboxs:
                gMilliseconds = gitem[4]
                if abs(gMilliseconds - cMilliseconds) <= lifeTime:
                    newgbboxs.append(gitem)
                    cbox = gitem[1]
                    # print(dots)
                    # print(gitem[1])
                    # print("gitem[1]")
                    if dist(dots, cbox) < d:
                        d = dist(dots, cbox)
                        if d < dpix:
                            name = zdata[gitem[3]]['name']
            gbboxs = newgbboxs
            fontScale = 2
            color=(0, 255, 0)
            cv2.putText(img, name,
                        (dots[0], dots[1] - 20), cv2.FONT_HERSHEY_COMPLEX,
                        fontScale, color, 3)
            # cv2.putText(img, name,
            #             (dots[0], dots[1] - 20), cv2.FONT_HERSHEY_COMPLEX,
            #             0.5, (255, 0, 255), 1)

    return img, gbboxs


def dist(dots, box):
    d = 0
    x1, y1, w1, h1 = dots
    x2, y2, w2, h2 = box
    xx1 = x1 + w1 / 2
    yy1 = y1 + h1 / 2
    xx2 = x2 + w2 / 2
    yy2 = y2 + h2 / 2
    d = np.sqrt((xx1 - xx2) ** 2 + (yy1 - yy2) ** 2)
    return d


def toPG(connection, img, bbox):
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    # _, data = cv2.imencode('.jpg', img, encode_param)
    # frame = data.tobytes()
    frame = simplejpeg.encode_jpeg(image=img, quality=90)
    milliseconds = int(time.time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # print(dt)
    score = milliseconds
    cursor = connection.cursor()
    bbox = json.dumps(str(bbox))
    sql_insert_with_param = """INSERT INTO z1frame
                          (frame, milliseconds ,timestr, bbox)
                          VALUES (%s, %s, %s, %s);"""
    data_tuple = (frame, milliseconds, dt, bbox)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()


def fromPGZdata(connection):
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM public.zdata ORDER BY milliseconds DESC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    zjson = []
    milliseconds = 0
    if datarecord:
        id = datarecord[0]
        zjson = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        sql_delete_query = "Delete from public.zdata where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        if len(zjson) > 1:
            zjson = zjson.replace("'", "")
            zjson = zjson.replace("\"", "")
            import ast
            zjson = ast.literal_eval(zjson)
    return zjson, milliseconds


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    connection.autocommit = True
    # cursor = connection.cursor()
    # sql_delete_query = "Delete from public.z1frame"
    # cursor.execute(sql_delete_query)
    # connection.commit()
    # sql_delete_query = "Delete from public.zdata"
    # cursor.execute(sql_delete_query)
    # connection.commit()
    # captpath = ".\\capture\\"
    # stream_params = {"-input_framerate": 10, "-livestream": True}
    # filelist = [f for f in os.listdir(captpath)]
    # for f in filelist:
    #     os.remove(os.path.join(captpath, f))
    zdata = zd.load()
    lifeTime = 1000 * 5
    number_of_processing_frame = 7
    HIGH_VALUE = 10000
    WIDTH = HIGH_VALUE
    HEIGHT = HIGH_VALUE
    cap = cv2.VideoCapture(1)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(width, height)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.25:554/ISAPI/Streaming/Channels/1")
    # cap = cv2.VideoCapture("d:\\test1.mp4")
    # cap = cv2.VideoCapture("d:\\test1_5mp.mp4")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    with pyvirtualcam.Camera(width=990, height=540, fps=30, fmt=PixelFormat.BGR) as cam:
        # with pyvirtualcam.Camera(width=990, height=540, fps=10, fmt=PixelFormat.BGR) as cam:
        # print(f'Using virtual camera: {cam.device}')
        # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        sframe = []
        count = 0
        pTime = 0
        # max_fps = cap.get(cv2.CAP_PROP_FPS)
        detection_score = 0.4  # порог чувствительности для поиска лица от 0 до 1
        minDetectionCon = 0.6
        mpFaceDetection = mp.solutions.face_detection
        # mpDraw = mp.solutions.drawing_utils
        faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence=minDetectionCon,
                                                      model_selection=1)
        gbboxs = []
        gdash = []
        DBsize = zd.getDBsize()
        while True:
            if DBsize != zd.getDBsize():
                DBsize = zd.getDBsize()
                zdata = zd.load()



            count += 1
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if len(frame) > 1:
                pTime = cTime
                # DrawFPS(frame, fps)
                img, bboxs = findFaces(frame, faceDetection)
                # print(bboxs)
                if count % number_of_processing_frame == 0:
                    count = 0
                    if len(bboxs) > 0:
                        toPG(connection, frame, bboxs)
                    else:
                        count -= 1
                zjson, milliseconds = fromPGZdata(connection)
                if int(milliseconds) > 0:
                    for item in zjson:
                        # iMilliseconds=item[3]
                        # print(item, iMilliseconds, milliseconds)
                        item.append(milliseconds)
                        gbboxs.append(item)
                    # cv2.imwrite(".\\capture\\" + str(milliseconds) + str(random.randint(0, 10 ** 10)) + ".jpg", frame)
                frame, gbboxs = DrawRectagle(img, bboxs, gbboxs, detection_score)
                # print(tuple(frame.shape[1::-1]))
                sframe = cv2.resize(frame, (990, 540))
                cam.send(sframe)
                cam.sleep_until_next_frame()
    connection.commit()
    connection.close()
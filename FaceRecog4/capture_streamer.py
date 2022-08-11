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
            # if len(bbox) > 1:
            #     img = fancyDraw(img, bboxs)
            # cv2.putText(img, f'{int(detection.score[0] * 100)}%',
            #             (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
            #             2, (255, 0, 255), 2)
    return img, bboxs


def DrawRectagle(img, bbox, detection_score, l=30, t=5, rt=1):
    for box in bbox:
        num = box[0]
        dots = box[1]
        score = box[2][0]
        # text =  box[2]
        if score >= detection_score:
            x, y, w, h = dots
            x1, y1 = x + w, y + h
            cv2.rectangle(img, dots, (255, 0, 255), rt)
            # # Top Left  x,y
            # cv2.line(img, (x, y), (x + l, y), (255, 0, 255), rt)
            # cv2.line(img, (x, y), (x, y + l), (255, 0, 255), rt)
            # # Top Right  x1,y
            # cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), rt)
            # cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), rt)
            # # Bottom Left  x,y1
            # cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
            # cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
            # # Bottom Right  x1,y1
            # cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), rt)
            # cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), rt)
    return img


def toPG(connection, img, bbox):
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    # _, data = cv2.imencode('.jpg', img, encode_param)
    # frame = data.tobytes()
    frame = simplejpeg.encode_jpeg(image=img, quality=70)
    milliseconds = int(time.time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # print(dt)
    score = milliseconds
    cursor = connection.cursor()
    bbox = str(bbox)
    sql_insert_with_param = """INSERT INTO z1frame
                          (frame, milliseconds ,timestr, bbox)
                          VALUES (%s, %s, %s, %s);"""
    data_tuple = (frame, milliseconds, dt, bbox)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.z1frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    # sql_delete_query = "Delete from public.z2frame"
    # cursor.execute(sql_delete_query)
    # connection.commit()

    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.25:554/ISAPI/Streaming/Channels/1")
    cap = cv2.VideoCapture("d:\\test1.mp4")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    with pyvirtualcam.Camera(width=990, height=540, fps=30, fmt=PixelFormat.BGR) as cam:
        # with pyvirtualcam.Camera(width=990, height=540, fps=10, fmt=PixelFormat.BGR) as cam:
        # print(f'Using virtual camera: {cam.device}')
        # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        sframe = []
        number_of_processing_frame = 3
        count = 0
        pTime = 0
        max_fps = cap.get(cv2.CAP_PROP_FPS)
        detection_score = 0.6  # порог чувствительрности для поиска лица от 0 до 1
        minDetectionCon = 0.6
        mpFaceDetection = mp.solutions.face_detection
        # mpDraw = mp.solutions.drawing_utils
        faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence=minDetectionCon,
                                                      model_selection=1)
        while True:
            count += 1
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            # frame[:] = cam.frames_sent % 255  # grayscale animation
            # frame = fromPG(connection)
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if len(frame) > 1:
                pTime = cTime
                # DrawFPS(frame, fps)
                #
                img, bboxs = findFaces(frame, faceDetection)
                # print(bboxs)
                if count % number_of_processing_frame == 0:
                    count = 0
                    toPG(connection, frame, bboxs)

                # тут рисовать имена
                DrawRectagle(img, bboxs, detection_score)

                sframe = cv2.resize(frame, (990, 540))
                cam.send(sframe)
                cam.sleep_until_next_frame()

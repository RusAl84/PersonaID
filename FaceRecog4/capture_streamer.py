import datetime
import pyvirtualcam
from pyvirtualcam import PixelFormat
import numpy as np
import cv2
import psycopg2
import time
import os
import simplejpeg


def toPG(connection, img):
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    # _, data = cv2.imencode('.jpg', img, encode_param)
    # frame = data.tobytes()
    frame = simplejpeg.encode_jpeg(image=img, quality=70)
    milliseconds = int(time.time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # print(dt)
    score = milliseconds
    cursor = connection.cursor()
    sql_insert_with_param = """INSERT INTO z1frame
                          (frame, milliseconds ,timestr)
                          VALUES (%s, %s, %s);"""
    data_tuple = (frame, milliseconds, dt)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.z1frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    sql_delete_query = "Delete from public.z2frame"
    cursor.execute(sql_delete_query)
    connection.commit()

    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
    cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.25:554/ISAPI/Streaming/Channels/1")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    with pyvirtualcam.Camera(width=990, height=540, fps=30, fmt=PixelFormat.BGR) as cam:
        # with pyvirtualcam.Camera(width=990, height=540, fps=10, fmt=PixelFormat.BGR) as cam:
        print(f'Using virtual camera: {cam.device}')
        # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        sframe = []
        number_of_processing_frame = 3
        count = 0
        while True:
            count += 1
            # frame[:] = cam.frames_sent % 255  # grayscale animation
            # frame = fromPG(connection)
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if len(frame) > 1:
                sframe = cv2.resize(frame, (990, 540))
                cam.send(sframe)
                cam.sleep_until_next_frame()
                if count % number_of_processing_frame == 0:
                    count = 0
                    toPG(connection, frame)

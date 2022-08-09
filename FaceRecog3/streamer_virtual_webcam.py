import datetime

import pyvirtualcam
import numpy as np
import cv2
import psycopg2
import time
import os
from pyvirtualcam import PixelFormat


def fromPG(connection):
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z2frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = []
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        cmilliseconds = int(time.time() * 1000)
        # if abs(milliseconds - cmilliseconds) > 5000:
        #     sql_delete_query = "Delete from public.z1frame"
        # else:
        #     sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        sql_delete_query = "Delete from public.z2frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now) + " " + timestr)
        # img = bytearray(frame)
        # img = frame
        # print(img)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


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

    with pyvirtualcam.Camera(width=990, height=540, fps=30, fmt=PixelFormat.BGR) as cam:
        # with pyvirtualcam.Camera(width=990, height=540, fps=10, fmt=PixelFormat.BGR) as cam:
        print(f'Using virtual camera: {cam.device}')
        # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        frame = []
        while True:
            # frame[:] = cam.frames_sent % 255  # grayscale animation
            frame = fromPG(connection)
            if len(frame) > 1:
                # frame = cv2.resize(frame, (990, 540))
                cam.send(frame)
                cam.sleep_until_next_frame()

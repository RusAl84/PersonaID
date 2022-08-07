import cv2
import os
# import numpy as np
# from PIL import ImageFont, ImageDraw, Image
from time import time

from flask import Flask, render_template, Response
import cv2
import redis
import numpy as np
import datetime
import psycopg2
import time

video_name = 'video.mp4'


def fromPG(connection):
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z2frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
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
        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        img = bytearray(frame)
        # print(img)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


if __name__ == '__main__':
    # images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    # frame = cv2.imread(os.path.join(image_folder, images[0]))
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    # images = []
    # for i in range(20):
    #     frame = fromPG(connection)
    #     height, width, layers = frame.shape
    #     images.append(frame)
    #     video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    # for image in images:
    #     video.write(image)
    # cv2.destroyAllWindows()
    # video.release()

    frameSize = (990, 540)
    out = cv2.VideoWriter('1.mp4', cv2.VideoWriter_fourcc(*'H264'), 10, frameSize)
    for i in range(50):
        frame = fromPG(connection)
        out.write(frame)
    out.release()

import datetime
import cv2
import psycopg2
import time
import numpy as np


def toPG(r, img):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, data = cv2.imencode('.jpg', img, encode_param)
    frame = data.tobytes()
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
    postgreSQL_select_Query = "SELECT * FROM public.z1frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        # timestr = datarecord[3]
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        # img = bytearray(frame)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    # cursor = connection.cursor()
    # sql_delete_query = "Delete from public.z1frame"
    # cursor.execute(sql_delete_query)
    # connection.commit()
    # time.sleep(0.5)
    while True:
        frame = fromPG(connection)
        # frame = cv2.resize(frame, (495, 270))
        if len(frame)>1:
            frame = cv2.resize(frame, (990, 540))
            # frame = cv2.resize(frame, (495, 270))
            # 990 540
            # 660 360
            # 495 270
            # 396 216
            # 330 180
            toPG(connection, frame)
            # time.sleep(0.003)

import cv2
from time import sleep
import psycopg2
import numpy as np
import datetime

def fromPG(r):
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z1frame ORDER BY milliseconds ASC LIMIT 1"

    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]


        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser",
                                  # пароль, который указали при установке PostgreSQL
                                  password="pgpwd4persona",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="personadb")

    key = 0
    while key != 27:
        img = fromPG(connection)
        if img != []:
            # img = cv2.resize(img, (960, 540))
            # img = cv2.resize(img, (640, 360))
            cv2.imshow("image", img)
        key = cv2.waitKey(10) & 0xFF
    # cv2.destroyAllWindows()
    if connection:
        # cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
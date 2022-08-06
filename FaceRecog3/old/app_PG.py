# import numpy as np
# from PIL import ImageFont, ImageDraw, Image
from time import time

from flask import Flask, render_template, Response
import cv2
import redis
import numpy as np
import datetime
import psycopg2

app = Flask(__name__)

def fromPG(connection):
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
        cmilliseconds = int(time() * 1000)
        # if abs(milliseconds - cmilliseconds) > 5000:
        #     sql_delete_query = "Delete from public.z1frame"
        # else:
        #     sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def gen_frames():
    count = 0
    connection = psycopg2.connect(user="personauser",
                                  # пароль, который указали при установке PostgreSQL
                                  password="pgpwd4persona",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.z1frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    while True:
        img=[]
        img = fromPG(connection)
        if img != []:
            # print(img)
            # cv2.imshow("image", img)
            img = cv2.resize(img, (960, 540))
            # cv2.imwrite("d:\\2.jpg", img)
            # frame= cv2.imencode(".jpg", img)[1].tobytes()
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            # print(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result





@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    # return render_template('index.html')
    # return render()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)

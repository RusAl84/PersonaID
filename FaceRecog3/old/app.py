# import numpy as np
# from PIL import ImageFont, ImageDraw, Image
from flask import Flask, render_template, Response
import cv2
import redis
import numpy as np
import datetime

app = Flask(__name__)


def fromRedis(r):
    data=[]
    # data = r.zrange("z1frame", 0, -1, withscores=True)
    data = r.zrange("z1frame", -2, -1, withscores=True)
    img = []
    if data:
        score = int(data[0][1])
        data = list(data[0])[0]
        r.zremrangebyscore("z1frame", score, score)
        # print(score)
        dt = datetime.datetime.fromtimestamp(score / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        # print(( now - dt) )
        # print(data)
        img = np.asarray(bytearray(data), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def gen_frames():
    count = 0
    r = redis.Redis(host='localhost', port=6379, db=0)
    # r.flushall()
    while True:
        img=[]
        img = fromRedis(r)
        if img != []:
            # print(img)
            # cv2.imshow("image", img)
            img = cv2.resize(img, (960, 540))
            # cv2.imwrite("d:\\2.jpg", img)
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
    app.run(debug=True)

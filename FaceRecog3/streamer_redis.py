import cv2
from time import sleep
import struct
import redis
import numpy as np
import datetime

def fromRedis(r):
    data = r.zrange("z1frame", 0, -1, withscores=True)
    # data = r.zrange("z1frame", 0, -1)
    img = []
    if data:
        score = int(data[0][1])
        data = data[0][0]
        r.zremrangebyscore("z1frame", score, score)
        # print(score)
        dt = datetime.datetime.fromtimestamp(score / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        img = np.asarray(bytearray(data), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    key = 0
    while key != 27:
        img = fromRedis(r)
        if img != []:
            # img = cv2.resize(img, (640, 360))
            cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF
    # cv2.destroyAllWindows()
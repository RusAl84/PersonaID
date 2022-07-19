import cv2
from time import sleep
import struct
import redis
import numpy as np


def fromRedis(r):
    data = r.zrange("z1frame", 0, -1, withscores=True)
    # data = r.zrange("z1frame", 0, -1)
    score = data[1][1]
    data = data[0]
    # print(data)
#     r.zrem("z1frame", score)
    r.zremrangebyscore("z1frame", int(score), int(score))
    # print(score)
    return data


if __name__ == '__main__':
    # Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)

    key = 0
    while key != 27:
        img = fromRedis(r)
        img = np.asarray(bytearray(img[0]), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

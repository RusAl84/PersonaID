import cv2
from time import sleep
import struct
import redis
import numpy as np


def fromRedis(r):
    # """Retrieve Numpy array from Redis key 'n'"""
    encoded = r.zrange("z1frame", 0, -1)
    return encoded
    # h, w = struct.unpack('>II',encoded[:8])
    # a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
    # return a


if __name__ == '__main__':
    # Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)

    key = 0
    while key != 27:
        img = fromRedis(r)
        # print(img)
        # img = np.array(img.split(' '), dtype=float)
        # cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
        # convert to numpy array

        img = np.asarray(bytearray(img[0]), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        #
        # print(img)
        # print(f"read image with shape {img.shape}")
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

import datetime
from time import sleep
import numpy as np
import cv2
import redis

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        data=[]
        data = r.zrange("z1frame", -10, -10, withscores=True)
        if data:
            score = int(data[0][1])
            data = list(data[0])[0]
            r.zremrangebyscore("z1frame", score, score)
            # r.zremrangebyscore("z1frame", score, score)
            # print(score)
            dt = []
            dt = datetime.datetime.fromtimestamp(score / 1000.0)
            now = datetime.datetime.now()
            print(str(dt.time()) + " " + str(now))
            img = []
            img = np.asarray(bytearray(data), dtype="uint8")
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (960, 540))
            # print(img)
            cv2.imshow("dsdsds", img)
            key = cv2.waitKey(10)
            if key == ord('q'):
                # self.capture.release()
                cv2.destroyAllWindows()
                exit(1)
            # sleep(0.05)

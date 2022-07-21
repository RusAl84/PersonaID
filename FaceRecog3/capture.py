import datetime

import cv2
import redis
from time import time


def toRedis(r, img):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
    _, data = cv2.imencode('.jpg', img, encode_param)
    data = data.tobytes()
    milliseconds = int(time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    print(dt)
    score = milliseconds
    r.zadd("z1frame", {data: score})
    return


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    # r.flushdb()
    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
    cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.25:554/ISAPI/Streaming/Channels/1")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # if cv2.waitKey(1) == ord('q'):
        #     break
        # frame = cv2.resize(frame, (960, 540))
        toRedis(r, frame)
    # cap.release()
    # cv2.destroyAllWindows()

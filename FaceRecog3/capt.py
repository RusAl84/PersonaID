import cv2
import struct
import redis
import numpy as np
import time

def toRedis(r, img):
    """Store given Numpy array 'a' in Redis under key 'n'"""
    # h, w = img.shape[:2]
    # shape = struct.pack('>II', h, w)
    # encoded = shape + img.tobytes()

    # Store encoded data in Redis
    # r.set(n, encoded)
    #
    # data = str(encoded)
    data = str(str(img))
    score = time.time_ns()
    r.zadd("z1frame", {data: score})
    return


if __name__ == '__main__':

    # Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)

    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
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

        if cv2.waitKey(1) == ord('q'):
            break
        toRedis(r, frame)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    #
    # cap.release()
    # cv2.destroyAllWindows()
import datetime
import cv2
import psycopg2
import time


def toPG(r, img):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, data = cv2.imencode('.jpg', img, encode_param)
    frame = data.tobytes()
    milliseconds = int(time.time() * 1000)
    dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
    # print(dt)
    score = milliseconds
    cursor = connection.cursor()
    sql_insert_with_param = """INSERT INTO z1frame
                          (frame, milliseconds ,timestr)
                          VALUES (%s, %s, %s);"""
    data_tuple = (frame, milliseconds, dt)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit()
    return


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
    # cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.23:554/ISAPI/Streaming/Channels/1")
    cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.88.25:554/ISAPI/Streaming/Channels/1")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        toPG(connection, frame)
        # time.sleep(0.1)
    if connection:
        connection.close()

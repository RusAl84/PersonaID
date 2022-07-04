import cv2
import numpy as np
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
vcap = cv2.VideoCapture("rtsp://admin:admin1234@192.168.1.64:554/Streaming/Channels/101", cv2.CAP_FFMPEG)
while True:
    ret, frame = vcap.read()
    if ret == False:
        print("Frame is empty")
        break;
    else:
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

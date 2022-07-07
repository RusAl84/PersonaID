import cv2

# cap = cv2.VideoCapture("rtsp://admin:xxxx@10.168.1.248:554/h264/ch1/main/av_stream")
cap = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")

out = cv2.VideoWriter("appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw, format=BGRx ! nvvidconv ! omxh264enc ! video/x-h264, stream-format=byte-stream ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=127.0.0.1 port=50001", cv2.CAP_GSTREAMER, 0, 25.0, (
1920,1080))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if out.isOpened():
            out.write(frame)
            print('writing frame')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
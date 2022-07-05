import numpy as np
from PIL import ImageFont, ImageDraw, Image
from flask import Flask, render_template, Response
import cv2
from FaceDetectionModule import FaceDetector
from FaceRecognitionModule import FaceRecognizer

app = Flask(__name__)

# camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture("rtsp://admin:FreePAS12@192.168.1.65:554/ISAPI/Streaming/Channels/101")
# camera = cv2.VideoCapture("Videos/6.mp4")
detector = FaceDetector(0.7)
# recognizer = FaceRecognizer("Faces",["Голованова","Горин","Григорьев","Кудж","Никонов","Русаков","Тимошенко","Трубиенко"])
recognizer = FaceRecognizer("Faces", ["Горин", "Русаков"])
every_nth_frame = 19
detection_life = 5
max_face_distance = 0.55


# 'rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def recognize(bboxs, frame):
    print(recognizer.recognize(bboxs, frame, max_face_distance))


def gen_frames():  # generate frame by frame from camera
    global my_threads
    count = 0
    while True:
        count = (count + 1) % every_nth_frame
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame, bboxs = detector.findFaces(frame, True)
            for bbox in bboxs:
                for k, v in recognizer.get_info(detection_life).items():
                    cx1 = bbox[1][0] + bbox[1][2] // 2
                    cy1 = bbox[1][1] + bbox[1][3] // 2
                    cx2 = v[0][1][0] + v[0][1][2] // 2
                    cy2 = v[0][1][1] + v[0][1][3] // 2
                    affordable_dist = (bbox[1][2] + bbox[1][3]) // 2
                    if (cx1 - cx2) ** 2 + (cy1 - cy2) ** 2 < affordable_dist ** 2:
                        # draw = ImageDraw.Draw(img_pil)
                        # draw.text((bbox[1][0], bbox[1][1] + bbox[1][3] + 20) ,  k, font = font, fill = (255, 0, 255, 255))
                        cv2.putText(frame, f'{k}', (bbox[1][0], bbox[1][1] + bbox[1][3] + 50), cv2.FONT_HERSHEY_COMPLEX,
                                    2, (255, 0, 255), 2)

            if count == 0:
                recognize(bboxs, frame)
                # print("!")

            frame = cv2.resize(frame, (1280, 720))

            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

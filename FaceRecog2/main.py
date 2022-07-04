import os.path
import threading
import time
import cv2
import face_recognition
import numpy as np
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from FaceDetectionModule import FaceDetector
import multiprocessing

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("1.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("2.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_images = [
    obama_image,
    biden_image
]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Бакаев АА",
    "Русаков АМ"
]

people_in_picture = []


def recognize(bboxs, frame):
    app = App.get_running_app()
    face_locations = [(bbox[1][1], bbox[1][0] + bbox[1][2], bbox[1][1] + bbox[1][3], bbox[1][0]) for bbox in bboxs]
    rgb_frame = frame[:, :, ::-1]
    face_names = []
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    print(face_names)

    id = 1
    pipLIFE = 5
    for kfn in known_face_names:
        if kfn in face_names:

            i = face_names.index(kfn)
            bbox = bboxs[i]

            X, Y, W, H = bbox[1]
            cropped_image = frame[Y:Y + H, X:X + W]

            if kfn in [pip[0] for pip in people_in_picture]:
                for pip in people_in_picture:
                    if pip[0] == kfn:
                        pip[1] = pipLIFE
                        pip[2] = id
                        pip[3] = cropped_image
            else:
                people_in_picture.append([kfn, pipLIFE, id, cropped_image])
            id += 2

    print([(pip[0], pip[1], pip[2]) for pip in people_in_picture])
    for pip in people_in_picture[:]:
        cv2.imwrite(os.path.join("Sources", "FaceImage" + str(pip[2]) + ".jpg"), pip[3])
        cv2.imwrite(os.path.join("Sources", "FaceImage" + str(pip[2] + 1) + ".jpg"),
                    cv2.cvtColor(known_images[known_face_names.index(pip[0])], cv2.COLOR_RGB2BGR))

        idx = pip[2]
        pip[1] -= 1
        if pip[1] == 0:
            people_in_picture.remove(pip)
            for pip2 in people_in_picture[:]:
                if pip2[2] > idx:
                    pip2[2] -= 2

    img = cv2.imread('Sources/FaceImage.jpg')
    for i in range(len(people_in_picture) * 2, 6):
        cv2.imwrite(os.path.join("Sources", "FaceImage" + str(i + 1) + ".jpg"), img)


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

    pass


class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        # self.capture = cv2.VideoCapture("Videos/4.mp4")
        self.capture = cv2.VideoCapture(0)

        # os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        # self.capture = cv2.VideoCapture("rtsp://admin:admin1234@192.168.1.64:554/Streaming/Channels/101",
        #                                 cv2.CAP_FFMPEG)
        self.detector = FaceDetector(0.5)
        fps = max(self.capture.get(cv2.CAP_PROP_FPS), 10)
        self.count = 0
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        self.count = (self.count + 1) % 10
        ret, frame = self.capture.read()
        if ret:

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

            if self.count == 0:
                frame, bboxs = self.detector.findFaces(frame, False)
                print(bboxs)

                pr = threading.Thread(target=recognize, args=(bboxs, frame))

                pr.start()

                app = App.get_running_app()
                for FaceImage in app.root.ids:
                    if FaceImage.__contains__("FaceImage"):
                        app.root.ids[FaceImage].reload()

                for pip in people_in_picture[:]:
                    app.root.ids["Label" + str(pip[2] // 2 + 1)].text = pip[0]
                for i in range(len(people_in_picture) * 2, 6):
                    app.root.ids["Label" + str((i) // 2 + 1)].text = "No Text"


class FaceDetectionApp(App):
    pass


if __name__ == '__main__':
    multiprocessing.freeze_support()
    FDapp = FaceDetectionApp()
    FDapp.run()

import cv2
import dlib
from PIL import Image
from recognition import compare

class FaceRecognition:
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.tracker = dlib.correlation_tracker()

    def track_object(self, frame):
        self.tracker.update(frame)
        dots = self.tracker.get_position()
        return dots

    def get_rectangle_corners(self, dots):
        left = round(dots.left())
        bottom = round(dots.bottom())
        right = round(dots.right())
        top = round(dots.top())

        return left, bottom, right, top

    def start_track(self, frame, dets):
        for d in dets:
            self.tracker.start_track(frame, dlib.rectangle(d.left(), d.top(), d.right(), d.bottom()))
            self.draw_rectangle(frame, dets)

    def put_predictions(self, frame, dets, name='Unknown'):
        try:
            cv2.putText(frame, name, (dets[0].right(), dets[0].top()), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        except IndexError:
            ...

    @staticmethod
    def draw_rectangle(frame, dets):
        d = dets[0]
        cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)

    def processing_video(self,cam_index):
        count = 0
        video = cv2.VideoCapture(cam_index)
        while video.isOpened():
            ret, frame = video.read()
            dets = self.face_detector(frame, 1)
            if len(dets) == 1:
            # if count in (5, 15):
                new_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                name = compare(new_frame, dets[0])
                self.start_track(frame, dets)
            else:
                dots = self.track_object(frame)
                left, bottom, right, top = self.get_rectangle_corners(dots)
                cv2.rectangle(frame, (left, bottom), (right, top), (0, 255, 0), 2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            self.put_predictions(frame, dets, name)
            count += 1
            # cv2.resizeWindow('name', 1280, 640)
            cv2.imshow('name', frame)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam_index = 1 # номер камеры
    FaceRecognition().processing_video(cam_index)

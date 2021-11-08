import face_recognition as fc
import numpy as np
from PIL import Image
import cv2

def load_file(filename):
    n_image = fc.load_image_file(filename)
    n_image_encoding = fc.face_encodings(n_image)[0]
    return  n_image_encoding

def load_face_photo():
    known_face_encodings = []
    known_names = []
    known_face_encodings.append(load_file(r'../FaceRecog/Photos/Rusal.jpg'))
    known_names.append('Русаков Алексей')
    return (known_names, known_face_encodings)



def get_coordinates(dets):
    left = dets.left()
    bottom = dets.bottom()
    right = dets.right()
    top = dets.top()

    return left, top, right, bottom


def eject_face(frame, dets):
    frame = Image.fromarray(frame)
    coordinates = get_coordinates(dets)
    face = frame.crop(coordinates)
    return np.array(face)


def compare(frame, dets):
    (known_names, known_face_encodings) = load_face_photo()
    frame = np.array(frame)
    face = eject_face(frame, dets)
    frame = cv2.resize(face, (0, 0), fx=0.25, fy=0.25)
    cv2.imshow('flex', frame)
    small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    stranger = fc.face_encodings(small_frame)
    try:
        result = fc.compare_faces(known_face_encodings, stranger[0])
        print("result")
        print(result)
        if any(result):
            name = known_names[result.index(True)]
        else:
            name = 'Unknown'
    except IndexError:
        name = 'Unknown'

    return name

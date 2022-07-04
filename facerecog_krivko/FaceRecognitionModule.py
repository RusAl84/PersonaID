import os
import time

import face_recognition
import numpy as np


class FaceRecognizer():
    def __init__(self,knownFacesFolder,knownNames):
        self.faces_info = {}
        self.known_images = []
        self.known_encodings = []
        for file in os.listdir(knownFacesFolder):
            print(file)
            image = face_recognition.load_image_file(os.path.join(knownFacesFolder,file))
            print(os.path.join(knownFacesFolder,file))
            self.known_images.append(image)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_encodings.append(face_encoding)
            self.known_names = []
        for name in knownNames:
            self.known_names.append(name)

    def get_info(self,detection_life):

        for k in self.faces_info.copy():
            if time.time() - self.faces_info[k][1] > detection_life:
                self.faces_info.pop(k)

        return self.faces_info

    def recognize(self,bboxs,frame,max_face_distance):
        face_locations = [(bbox[1][1], bbox[1][0] + bbox[1][2], bbox[1][1] + bbox[1][3], bbox[1][0]) for bbox in bboxs]
        rgb_frame = frame[:, :, ::-1]
        face_names = []
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and min(face_distances)<max_face_distance:
                name = self.known_names[best_match_index]
                print(name,face_distances)


            face_names.append(name)

        for i in range(len(face_names)):
            if face_names[i] != "Unknown":
                self.faces_info[face_names[i]] = (bboxs[i],time.time())

        return face_names


import dlib
import face_recognition
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import time
import playsound

# gerb load and scale
gerb_img = cv2.imread("Photos/MIREA_Gerb_Colour.png", -1)
gerb = cv2.resize(gerb_img, (0, 0), fx=0.075, fy=0.075)

# unicode text with ImageDraw
imageFont = ImageFont.truetype("arial.ttf", 20)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

def load_file(filename):
    n_image = face_recognition.load_image_file(filename)
    return face_recognition.face_encodings(n_image)[0]

known_face_encodings.append(load_file('Photos/Rusal.jpg'))
known_face_names.append("Русаков Алексей\nМихайлович")
known_face_encodings.append(load_file('Photos/Rusal2.jpg'))
known_face_names.append("Русаков Алексей\nМихайлович")
known_face_encodings.append(load_file('Photos/Bakaev_Anatolij.jpg'))
known_face_names.append("Бакаев Анатолий\nАлександрович")
known_face_encodings.append(load_file('Photos/Bakaev_Anatolij2.jpg'))
known_face_names.append("Бакаев Анатолий\nАлександрович")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
detector = dlib.get_frontal_face_detector()
count = 0
y_label_size = 50
x_label_size = 160
play_hello = True
while video_capture.isOpened():
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    faces = detector(frame, 1)
    # Only process every other frame of video to save time
    if len(faces) == 1:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        if count % 15 == 0:
            count = 0
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                name = u'Не узнаю вас'
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
        if len(face_names) == 0:
            face_names = ['Не узнаю вас',]
        count += 1
        if play_hello:
            playsound.playsound("Sounds/Hello_KBSP.mp3", False)
            play_hello = False
    elif len(faces) == 0:
        play_hello = True
    #process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom + y_label_size//2), (70, 55, 19), 2)

        # set label offset
        x_text_offset = left + gerb.shape[1] + 5
        y_text_offset = bottom - y_label_size//2
        # check right side (out of array exception)
        x_text_max = min(x_text_offset + x_label_size, frame.shape[1])
        y_text_max = min(y_text_offset + y_label_size, frame.shape[0])
        #generate text frame
        text_img = np.zeros((y_text_max - y_text_offset, x_text_max - x_text_offset, 3), np.uint8)
        img_pil = Image.fromarray(text_img)
        draw = ImageDraw.Draw(img_pil)
        #render text
        draw.text((0, 0), name, font=imageFont, fill=(255, 255, 255, 0))
        #put frame with text
        text_img = np.array(img_pil)
        #calculate alpha channels to delete black background
        text_alpha_chn = text_img[:, :, 2] / 255.0
        text_frame_alpha_chn = 1.0 - text_alpha_chn
        # Draw a label for text
        cv2.rectangle(frame, (left, bottom - 25), (max(x_text_max, right), y_text_max), (70, 55, 19), cv2.FILLED)
        for c in range(0, 2):
            frame[y_text_offset:y_text_max, x_text_offset:x_text_max, c] = \
                (text_alpha_chn * text_img[:, :, c] +
                 text_frame_alpha_chn * frame[y_text_offset:y_text_max,
                                   x_text_offset:x_text_max, c])

        # add gerb image
        x_gerb_offset = left
        y_gerb_offset = bottom - y_label_size//2
        # check right side (out of array exception)
        y_gerb_max = min(y_gerb_offset + gerb.shape[0], frame.shape[0])
        # add gerb image
        gerb_alpha_chn = gerb[:y_gerb_max-y_gerb_offset, :, 3] / 255.0
        frame_alpha_chn = 1.0 - gerb_alpha_chn
        for c in range(0, 3):
           frame[y_gerb_offset:y_gerb_max, x_gerb_offset:x_gerb_offset + gerb.shape[1], c] = \
                (gerb_alpha_chn * gerb[:y_gerb_max-y_gerb_offset, :, c] +
                 frame_alpha_chn * frame[y_gerb_offset:y_gerb_max,
                                  x_gerb_offset:x_gerb_offset + gerb.shape[1], c])

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

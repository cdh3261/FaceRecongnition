# face_recog.py
import face_recognition
import cv2
from . import camera
import os
import numpy as np


class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()
        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        dirname = 'C:/Users/multicampus/_dongho/First_PJT/Maria_Membership/newFace/'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def __del__(self):
        del self.camera
        # print(7)

    def get_frame(self):
        global stop, test, key
        # Grab a single frame of video

        # print(8)
        frame = self.camera.get_frame()
        # 여기가 다른데.....................################################
        frame = cv2.flip(frame, 1)
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # print(9)
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(
                rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(
                rgb_small_frame, self.face_locations)

            self.face_names = []
            self.face_percentage = []

            for face_encoding in self.face_encodings:
                # print(10)
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(
                    self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                test = round((1-min_value)*100, 1)
                if min_value < 0.3:  # 70프로매칭
                    index = np.argmin(distances)
                    name = self.known_face_names[index]
                    # print(11)
                    if name in face_recog.known_face_names:
                        # print(12)
                        # print('{}%'.format(test))
                        # print('{}님 무엇을 주문 하시겠습니까?'.format(name))
                        stop = 1
                        # 33
                        return name

                self.face_names.append(name)
                self.face_percentage.append(test)

        self.process_this_frame = not self.process_this_frame
        # print(13)
        # Display the results
        for (top, right, bottom, left), name, percent in zip(self.face_locations, self.face_names, self.face_percentage):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, str(percent), (left + 6, bottom + 18),
                        font, 1.0, (255, 255, 255), 1)
        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


face_recog = 0
stop = 0


def face():
    global face_recog, stop, key

    # if __name__ == '__main__':
    # stop = 0
    face_recog = FaceRecog()
    while True:
        frame = face_recog.get_frame()
        # show the frame
        if stop == 0:
            cv2.imshow("Face Check", frame)
        key = cv2.waitKey(1) & 0xff
        # if the `ESC` key was pressed, break from the loop
        if key == 32 or stop == 1:
            face_recog = 0
            cv2.destroyAllWindows()
            stop = 0
            if key == 32:
                return 'unknown'

            return frame
    print('Complete Face Recognition')

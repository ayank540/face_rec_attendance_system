import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from database import db

PATH = 'data_image'
images = []
classNames = []
myList = os.listdir(PATH)
date = datetime.now().date()

for cls in myList:
    currImg = cv2.imread(f'{PATH}/{cls}')
    images.append(currImg)
    classNames.append(os.path.splitext(cls)[0])

def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(className):
    roll, name = className.split(' ')
    time_ = datetime.now().strftime("%Hh:%Mm:%Ss")
    date_ = datetime.now().date()
    db.add_to_db(roll, name, date_, time_)


encodeListKnown = find_encodings(images)
print('Encoding completed')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)         # 1/4th of image size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    for encodeface, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeface)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeface)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

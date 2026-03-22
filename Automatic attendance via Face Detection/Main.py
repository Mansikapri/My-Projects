import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = "Attendance Images"
images =[]
classNames =[]
myList = os.listdir(path)
#print(myList)
for cli in myList:
    cuImg = cv2.imread(f'{path}/{cli}')
    images.append(cuImg)
    classNames.append(os.path.splitext(cli)[0])
#print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance register.csv','r+') as fp:
        myDatalist=fp.readlines()

        pnamelist = []
        for line in myDatalist:
            entry = line.split(',')
            pnamelist.append(entry[0])
        if name not in pnamelist:
            now = datetime.now()
            dtString = now.strftime('%H:%M')
            fp.writelines(f'\n{name},{dtString}')


encodelistun= findEncodings(images)
#print(len(encodelistun))

cap = cv2.VideoCapture(0)
print(('Encoding Completed'))
while True:
    success ,img =cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facecurrloc = face_recognition.face_locations(imgS)
    encode = face_recognition.face_encodings(imgS,facecurrloc)

    for encodeface, faceloc in zip(encode,facecurrloc):
        matches = face_recognition.compare_faces(encodelistun,encodeface)
        faceDis = face_recognition.face_distance(encodelistun,encodeface)
        #print(faceDis)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].capitalize()
            #print(name)
            y1,x2,y2,x1=faceloc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,255),2)
            markAttendance(name)
        else:
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 0), cv2.FILLED)
            cv2.putText(img,'Unknown', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)



    cv2.imshow('webcam',img)
    cv2.waitKey(1)

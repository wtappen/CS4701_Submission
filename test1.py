import numpy as np 
import cv2 as cv
cascadeLoc = 'cascades/data/haarcascade_frontalface_alt2.xml'
face_cascade = cv.CascadeClassifier(cascadeLoc)

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        color = (255,0,0)
        stroke = 2
        cv.rectangle(frame, (x,y), (x+w, y+h), color, stroke)


    cv.imshow('frame', frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()




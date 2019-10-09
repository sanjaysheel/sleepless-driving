import cv2
from functools import wraps
from pygame import mixer
import time
lastsave = 0
def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        global lastsave
        if time.time() - lastsave > 3:
            lastsave = time.time()
            tmp.count = 0
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
@counter
def closed():
  print("Eye Closed")
def openeye():
  print("Eye is Open")
def sound():
    mixer.init()
    mixer.music.load('sound.mp3')
    mixer.music.play()
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Edge = cv2.Laplacian(img, cv2.CV_64F)
    faces = face_cascade.detectMultiScale(gray, 1.1,4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 3)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        roi_Edge = Edge[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if eyes is not ():
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 3)
                cv2.rectangle(roi_gray, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 3)
                cv2.rectangle(roi_Edge, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 3)
                openeye()
        else:
           closed()
           if closed.count == 3:
               sound()
    cv2.imshow('Shyam', img);cv2.imshow('Gray_Scale_Image',gray);cv2.imshow('Edge_Image',Edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

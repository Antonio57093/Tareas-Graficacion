# Segmentacion en video.py

```python
"""
PROGRAMA: Segmentacion de color en video
DESCRIPCIÓN:
   Este programa aplica segmentación de color en tiempo real usando la cámara web.
   Convierte los fotogramas del video al espacio HSV y filtra colores dentro de un
   rango específico para mostrar solo las zonas de interés.
"""

#Segmentacion de color en video

import cv2 as cv
import numpy as np

cap=cv.VideoCapture(0)
while(True):
    ret,img =cap.read()
    if ret:
        cv.imshow('video',img)
        hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
        uba=(90,255,255)
        ubb=(40,40,40)
        mask=cv.inRange(hsv,ubb,uba)
        res=cv.bitwise_and(img, img,mask=mask)
        cv.imshow('res',res)
        cv.imshow('mask',mask)
        k=cv.waitKey(1) & 0xFF
        if k==27:
            break
    else:
        break
cap.release()
cv.destroyAllWindows()

```
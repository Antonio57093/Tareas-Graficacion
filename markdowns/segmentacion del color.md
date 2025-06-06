# segmentacion del color.py

```python
"""
PROGRAMA:Segmentacion de color 
DESCRIPCIÓN:
   Este programa realiza segmentación de color en una imagen cargada, utilizando el
   espacio de color HSV y máscaras binarias. Detecta zonas rojas (por ejemplo, manzanas)
   mediante rangos específicos y muestra el resultado segmentado con OpenCV.
"""

import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy

img = cv.imread('manzanas.jpeg',1)
hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)

uba=(10,255,255)
ubb=(0,100,100)

uba2=(180,255,255)
ubb2=(172,100,100)
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
cv.imshow('mask1',mask1)
cv.imshow('mask2',mask2)
cv.imshow('res',res)


cv.waitKey(0)
cv.destroyAllWindows
```
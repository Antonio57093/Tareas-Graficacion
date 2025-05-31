# dividir.py

```python
import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy

img = cv.imread('girasol.jpeg',1)
img2=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('img original ',img2)


x,y=img2.shape[:2]
print(x,y)
for i in range (x):
    for j in range (y):
        img2[i,j]=255-img2[i,j]  #operador puntual

cv.imshow('img2 ',img2)

cv.waitKey (0)
cv.destoyAllWindows()


```
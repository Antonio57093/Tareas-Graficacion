# actividad2.py

```python

"""
PROGRAMA: DETECTOR DE COLORES BÁSICO    
DESCRIPCIÓN: Este programa detecta y muestra por separado los objetos rojos, 
verdes, azules, amarillos y celestes en una imagen .
"""


import cv2 as cv   #importa openCv

img = cv.imread('objetos.jpg',1)
hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)

uba=(10,255,255)    #Filtra color rojo
ubb=(0,100,100)
uba2=(180,255,255)  
ubb2=(172,100,100)      ####
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
#cv.imshow('mask1',mask1)
#cv.imshow('mask2',mask2)
cv.imshow('Rojo',res) #color rojo


uba=(40,255,255)    #Filtra color Verde
ubb=(50,100,100)
uba2=(70,255,255)  
ubb2=(50,100,100)      ####
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
#cv.imshow('mask1',mask1)
#cv.imshow('mask2',mask2)
cv.imshow('Verde',res) #color Verde

uba=(90,255,255)    #Filtra color Azul
ubb=(100,100,100)
uba2=(130,255,255)  
ubb2=(100,100,100)      ####
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
#cv.imshow('mask1',mask1)
#cv.imshow('mask2',mask2)
cv.imshow('Azul',res) #color Azul

uba=(29,255,255)    #Filtra color Amarillo
ubb=(32,100,100)
uba2=(40,255,255)  
ubb2=(32,100,100)      ####
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
#cv.imshow('mask1',mask1)
#cv.imshow('mask2',mask2)
cv.imshow('Amarillo',res) #color Amarillo

uba=(81,255,255)    #Filtra color Celeste
ubb=(85,100,100)
uba2=(92,255,255)  
ubb2=(85,100,100)      ####
mask1=cv.inRange(hsv,ubb,uba)
mask2=cv.inRange(hsv,ubb2,uba2)
mask=mask1+mask2
res=cv.bitwise_and(img,img,mask=mask)
#cv.imshow('mask1',mask1)
#cv.imshow('mask2',mask2)
cv.imshow('Celeste',res) #color Celeste




cv.waitKey(0)
cv.destroyAllWindows
```
import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy

img = np.ones((500,500),dtype=np.uint8)*240

#Primer capa
for i in range (475,500):
    for j in range (75,275):
        img[i,j]=0
        
for i in range (475,500):
    for j in range (350,450):   
        img[i,j]=0  


#Segunda capa
for i in range (450,475):
    for j in range (50,75):
        img[i,j]=0 

for i in range (450,475):
    for j in range (250,475):
        img[i,j]=0 

#Tercera capa
for i in range (425,450):
    for j in range (25,50):
        img[i,j]=0 

for i in range (425,450):
    for j in range (75,175):
        img[i,j]=0 

for i in range (425,450):
    for j in range (325,500):
        img[i,j]=0 

#Cuarta capa
for i in range (400,425):
    for j in range (0,25):
        img[i,j]=0 

for i in range (400,425):
    for j in range (175,200):
        img[i,j]=0 

for i in range (400,425):
    for j in range (325,500):
        img[i,j]=0 


#quinta capa
for i in range (375,400):
    for j in range (0,25):
        img[i,j]=0 

for i in range (375,400):
    for j in range (325,500):
        img[i,j]=0 

#sexta capa
for i in range (350,375):
    for j in range (0,25):
        img[i,j]=0 

for i in range (350,375):
    for j in range (75,100):
        img[i,j]=0 

for i in range (350,375):
    for j in range (325,500):
        img[i,j]=0 

#septima capa
for i in range (325,350):
    for j in range (0,25):
        img[i,j]=0 

for i in range (325,350):
    for j in range (50,125):
        img[i,j]=0 

for i in range (325,350):
    for j in range (325,500):
        img[i,j]=0 


#octava capa
for i in range (300,325):
    for j in range (0,125):
        img[i,j]=0 


for i in range (300,325):
    for j in range (325,500):
        img[i,j]=0 

#novena capa
for i in range (275,300):
    for j in range (25,75):
        img[i,j]=0 

for i in range (275,300):
    for j in range (175,200):
        img[i,j]=0 

for i in range (275,300):
    for j in range (250,275):
        img[i,j]=0 


for i in range (275,300):
    for j in range (325,500):
        img[i,j]=0 



#decima capa
for i in range (250,275):
    for j in range (75,125):
        img[i,j]=0 

for i in range (250,275):
    for j in range (175,200):
        img[i,j]=0 

for i in range (250,275):
    for j in range (250,275):
        img[i,j]=0 

for i in range (250,275):
    for j in range (350,475):
        img[i,j]=0 


#onceava capa
for i in range (225,250):
    for j in range (125,175):
        img[i,j]=0 

for i in range (225,250):
    for j in range (350,475):
        img[i,j]=0 

#doceava capa
for i in range (200,225):
    for j in range (150,200):
        img[i,j]=0 

for i in range (200,225):
    for j in range (375,450):
        img[i,j]=0 

#treceava capa
for i in range (175,200):
    for j in range (175,200):
        img[i,j]=0 

for i in range (175,200):
    for j in range (400,450):
        img[i,j]=0 

#catorceava capa
for i in range (150,175):
    for j in range (200,250):
        img[i,j]=0 

for i in range (150,175):
    for j in range (375,425):
        img[i,j]=0 

#quinceava capa
for i in range (125,150):
    for j in range (225,375):
        img[i,j]=0 

cv.imshow('pixelart',img)
cv.waitKey (0)
cv.destoyAllWindows()
        
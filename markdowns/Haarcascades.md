# Haarcascades.py

```python
"""
PROGRAMA: Detección de Rostros con Haar Cascades y Efectos Visuales
DESCRIPCIÓN:
El script utiliza un clasificador Haar Cascade para detectar rostros en tiempo real mediante la cámara. Agrega elementos visuales como ojos, pupilas y una "sonrisa" dibujados sobre la cara detectada para un efecto caricaturesco.
"""
import cv2 as cv 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    for(x,y,w,h) in rostros:
        res = int((w+h)/8)
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5)
        
        #coordenadas,rectangulo,BGR,Ancho
        img = cv.rectangle(img, (x + int (h/2),y+int(w/2)), (x+int (h),y+int (w)), (0,255,0),-1 )
        

        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 5, (0, 0, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 5, (0, 0, 255), -1 )

    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()
```
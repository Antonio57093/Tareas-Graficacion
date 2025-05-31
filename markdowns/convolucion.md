# convolucion.py

```python

import cv2 as cv
import numpy as np

img = cv.imread('girasol.jpeg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Definir el factor de escala
scale_x, scale_y = 1,1
scaled_img2=cv.resize(img,None,fx=scale_x,fy=scale_y)
# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)
a= 1/9
b = np.array([[a,a,a],[a,a,a],[a,a,a]])


# Aplicar el escalado
for i in range(x):
    for j in range(y):
                   scaled_img2[i, j] = img[i,j]
                   

                   
# Mostrar la imagen original y la escalada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada con funcion de cv', scaled_img2)
cv.waitKey(0)
cv.destroyAllWindows()
```
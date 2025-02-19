import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Palito

#punto inicial,punto final,color,grosor
cv.line(img, (250, 250), (250, 400), (0, 0, 0), 5)

# maceta
cv.rectangle(img, (200, 400), (300, 450), (0, 0, 100), -1)
cv.rectangle(img, (220, 450), (280, 490), (0, 0, 100), -1)

# petalos
cv.circle(img, (250, 200), 50, (218, 118, 10), 3)
cv.circle(img, (200, 250), 50, (218, 118, 10), 3)
cv.circle(img, (300, 250), 50, (218, 118, 10), 3)
cv.circle(img, (250, 300), 50, (218, 118, 10), 3)

#cuadrado del centro

#punto inicial,punto final,color,grosor
cv.rectangle(img, (235, 235), (265, 265), (10, 214, 218), -1)


# Mostrar la imagen
cv.imshow('Flor Geométrica', img)
cv.waitKey(0)
cv.destroyAllWindows()


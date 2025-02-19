import cv2 as cv
import numpy as np
import math

def punto(centro, punto, angulo):
    angulo = math.radians(angulo)
    ox, oy = centro
    px, py = punto
    qx = ox + math.cos(angulo) * (px - oy) - math.cos(angulo) * (py - ox)
    qy = oy + math.sin(angulo) * (px - oy) + math.sin(angulo) * (py - ox)
    return int(qx), int(qy)

def flor(img, angulo):
    centro = (250, 250)
    petalos = [(250, 200), (200, 250), (300, 250), (250, 300)]
    colorpetalos = (218, 118, 10)
    radio_petalo = 50

    # Palito
    cv.line(img, (250, 250), (250, 400), (0, 0, 0), 5)

    # Maceta
    cv.rectangle(img, (200, 400), (300, 450), (0, 0, 100), -1)
    cv.rectangle(img, (220, 450), (280, 490), (0, 0, 100), -1)

    # Pétalos rotados
    for petal in petalos:
        petalo_rotado = punto(centro, petal, angle)
        cv.circle(img, petalo_rotado, radio_petalo, colorpetalos, -1)

    # Cuadrado del centro
    cv.rectangle(img, (235, 235), (265, 265), (10, 214, 218), -1)

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

angle = 0
while True:
    img_copy = img.copy()
    flor(img_copy, angle)
    cv.imshow('Flor ', img_copy)
    angle += 1
    if cv.waitKey(30) & 0xFF == 27: 
        break

cv.destroyAllWindows()


import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()  
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
p0 = np.array([(100, 150), (150, 150), (200, 150),
               (100, 200), (150, 200), (200, 200),
               (100, 250), (150, 250), (200, 250)])

p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(100, 100), (200, 100), (300, 100), (400, 100)])
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]
        direction_sum = np.zeros(2)
        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())
            direction = (a - c, b - d)
            dist = np.linalg.norm(nv.ravel() - vj.ravel())
            direction_sum += direction

            frame = cv.line(frame, (c, d), (a, b), (0, 0, 255), 2)
            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)
            height, width = frame.shape[:2] 
            cv.rectangle(frame, (20, 20), (width - 20, height - 20), (234, 43, 34), 5)
            cv.putText(frame, f'{direction}', (a, b - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Calcular la posición del círculo basado en la dirección promedio
        puntos = len(bp1)
        if puntos > 0:
            direccion = direction_sum / puntos
            circuloc = (int(width/2 + direccion[0]), int(height/2 + direccion[1]))

            # Dibujar el círculo en la posición calculada
            cv.circle(frame, circuloc, 30, (0, 255, 255), -1)

        cv.imshow('ventana', frame)

        vgris = fgris.copy()

    if (cv.waitKey(1) & 0xff) == 27:
        break

cap.release()
cv.destroyAllWindows()

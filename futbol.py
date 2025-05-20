import numpy as np
import cv2 as cv

# Iniciar la captura de video desde la cámara
cap = cv.VideoCapture(0)

# Parámetros para el flujo óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer el primer frame de la cámara
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posición inicial de la pelotita (un único punto en el centro de la imagen)
initial_ball_pos = np.array([[300, 250]], dtype=np.float32)
ball_pos = initial_ball_pos[:, np.newaxis, :]


while True:
    # Capturar el siguiente frame
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]     #calculamos la altura y ancho de la ventana
    frame = cv.flip(frame, 1)
    # Convertir el frame a escala de grises
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico para mover la pelotita
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    # Si se detecta el nuevo movimiento, actualizar la posición de la pelotita
    if new_ball_pos is not None:
        ball_pos = new_ball_pos

        # Dibujar la pelotita en su nueva posición
        a, b = ball_pos.ravel()
        cv.putText(frame,f'({int(a)},{int(b)})',(int (a-30),int(b-30)), cv.FONT_HERSHEY_SIMPLEX,0.7,(0,25,235),2)
        # Verificar si la pelotita está fuera del rectángulo
        if not (20 < b < 500 - 20 and 20 < a < 500 - 20):
            ball_pos = initial_ball_pos[:, np.newaxis, :]  # Restablecer la posición de la pelotita

        frame = cv.circle(frame, (int(a), int(b)), 20, (0, 255, 0), -1)
        
    cv.rectangle(frame, (20, 20), (width - 20, height - 20), (234, 43, 34), 5)
    # Mostrar solo una ventana con la pelotita en movimiento
    cv.imshow('Pelota en movimiento', frame)

    # Actualizar el frame anterior para el siguiente cálculo
    prev_gray = gray_frame.copy()

    # Presionar 'Esc' para salir
    if cv.waitKey(30) & 0xFF == 27:
        break

# Liberar la captura y destruir todas las ventanas
cap.release()
cv.destroyAllWindows()

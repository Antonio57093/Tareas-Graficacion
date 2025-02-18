import cv2
import numpy as np  

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Crear una imagen negra para dibujar el rastro
trail = None

# Permitir que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo durante unos segundos
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()

# Definir variables para el seguimiento del objeto
prev_center = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Inicializar la imagen del rastro si aún no se ha creado
    if trail is None:
        trail = np.zeros_like(frame)

    # Convertir el cuadro a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color del objeto a rastrear (verde, en este caso)
    lower_green = np.array([100, 240, 100])
    upper_green = np.array([110, 255, 255])

    # Crear una máscara que detecta el área verde
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Encontrar contornos del objeto
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Obtener el contorno más grande
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)

        if M["m00"] != 0:
            # Calcular el centro del objeto
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibujar el rastro solo si hay un punto anterior registrado
            if prev_center is not None:
                cv2.line(trail, prev_center, (cx, cy), (0, 0, 255), 5)  # Rojo

            # Actualizar el punto anterior
            prev_center = (cx, cy)

    # Invertir la máscara para obtener las áreas que no son verdes
    mask_inv = cv2.bitwise_not(mask)

    # Aplicar la máscara a la imagen original para mostrar solo las partes no verdes
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Aplicar la máscara al fondo para cubrir las partes verdes
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar ambas imágenes
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 

    # Superponer el rastro sobre la imagen final
    combined = cv2.addWeighted(final_output, 1, trail, 1, 0)

    # Mostrar los resultados
    cv2.imshow("Capa de Invisibilidad", combined)
    cv2.imshow("Rastro", trail)
    cv2.imshow('Mask', mask)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()

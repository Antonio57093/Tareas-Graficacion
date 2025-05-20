import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Función para determinar la letra según la posición de los dedos
def reconocer_letra(hand_landmarks, frame):
    h, w, _ = frame.shape  # Tamaño de la imagen
    
    # Obtener coordenadas de los puntos clave en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    # Obtener posiciones clave (puntas de los dedos)
    pulgar, indice, medio, anular, meñique = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20]

    # Mostrar los números de los landmarks en la imagen
    for i, (x, y) in enumerate(dedos):
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Puntos verdes
        cv2.putText(frame, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Dibujar coordenadas del pulgar
    cv2.putText(frame, f'({int(pulgar[0])}, {int(pulgar[1])})', (pulgar[0], pulgar[1] - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (23, 0, 0), 2, cv2.LINE_AA)

    # Calcular distancias en píxeles entre los dedos
    distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))
    distancia_indice_medio = np.linalg.norm(np.array(indice) - np.array(medio))
    distancia_anular_meñique = np.linalg.norm(np.array(anular) - np.array(meñique))
   
    # Lógica para reconocer algunas letras
    if distancia_pulgar_indice <140 and distancia_pulgar_indice >130 and distancia_indice_medio <30 and distancia_anular_meñique <30:
        return "A"  # Seña de la letra A (puño cerrado con pulgar al lado)
    elif distancia_pulgar_indice >105 and distancia_pulgar_indice<125 and distancia_anular_meñique >30 and distancia_anular_meñique <45:
        return "B"  # Seña de la letra B (todos los dedos estirados, pulgar en la palma)
    elif distancia_pulgar_indice > 50 and distancia_indice_medio > 50:
        return "C"  # Seña de la letra C (mano en forma de "C")

    return "Desconocido"

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Dibujar puntos de la mano y reconocer letras
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
             # Obtener las coordenadas del pulgar y el índice
            h, w, _ = frame.shape
            pulgar = hand_landmarks.landmark[4]
            indice = hand_landmarks.landmark[8]
            medio = hand_landmarks.landmark[12]
            anular= hand_landmarks.landmark[16]
            meñique = hand_landmarks.landmark[20]

            basemedio=hand_landmarks.landmark[9]
            basemeñique=hand_landmarks.landmark[17]
            baseindice=hand_landmarks.landmark[5]
            baseanular=hand_landmarks.landmark[13]
            
            # Calcular la distancia entre el pulgar y el índice
            
            # Convertir coordenadas normalizadas a píxeles
            pulgar_px = (int(pulgar.x * w), int(pulgar.y * h))
            indice_px = (int(indice.x * w), int(indice.y * h))
            anular_px = (int(anular.x * w), int(anular.y * h))
            meñique_px = (int(meñique.x * w), int(meñique.y * h))

            # Calcular la distancia entre el pulgar y el índice
            distancia = int(np.linalg.norm(np.array(pulgar_px) - np.array(indice_px)))
            #Calular la distancia entre el anular y el meñique
            distancia1 = int(np.linalg.norm(np.array(anular_px) - np.array(meñique_px)))
            
            # Mostrar la distancia en el video
            cv2.putText(frame, f"Pulgar indice: {distancia}px", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            
            cv2.putText(frame,f"anular menique: {distancia1} px", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            
            

            # Identificar la letra
            letra_detectada = reconocer_letra(hand_landmarks, frame)

            # Mostrar la letra en pantalla
            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video
    cv2.imshow("Reconocimiento de Letras", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
# proyecto.py

```python
"""
PROGRAMA: Proyecto de Reconocimiento de Gestos en Lengua de Señas Mexicana (LSM)
DESCRIPCIÓN:
   Este programa detecta gestos de manos en tiempo real usando la cámara web, MediaPipe y OpenCV.
   Reconoce letras y números en LSM (como "O", "E", "X", "4", "30".) a partir de la posición
   relativa de los dedos. Permite identificar combinaciones con ambas manos y mostrar el resultado
   en pantalla de forma visual.
"""
import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)  # Corregido "min_detection_confidence"
mp_drawing = mp.solutions.drawing_utils

def distancia(p1, p2):
    return np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def detectar_gesto(landmarks):
    # Puntos clave de los dedos
    pulgar_tip = landmarks.landmark[4]
    indice_tip = landmarks.landmark[8]
    medio_tip = landmarks.landmark[12]
    anular_tip = landmarks.landmark[16]
    menique_tip = landmarks.landmark[20]


    # Bases de los dedos (corregido: usamos "landmarks", no "hand_landmarks")
    base_indice = landmarks.landmark[5]
    base_medio = landmarks.landmark[9]
    base_anular = landmarks.landmark[13]
    base_menique = landmarks.landmark[17]
    palma_base = landmarks.landmark[0]

    # Distancias entre puntas de dedos
    d_pulgar_indice = distancia(pulgar_tip, indice_tip)
    d_pulgar_medio = distancia(pulgar_tip, medio_tip)
    d_pulgar_anular = distancia(pulgar_tip, anular_tip)
    d_pulgar_menique = distancia(pulgar_tip, menique_tip)
    d_indice_medio = distancia(indice_tip, medio_tip)

    # Distancias entre puntas y bases (para detectar curvatura)
    d_indice_base = distancia(indice_tip, base_indice)
    d_medio_base = distancia(medio_tip, base_medio)
    d_anular_base = distancia(anular_tip, base_anular)
    d_menique_base = distancia(menique_tip, base_menique)
    cv2.putText(frame, f"Pulgar indice: {d_pulgar_indice}px", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)


    # Gestos
    if (d_pulgar_indice < 0.05 and d_pulgar_medio < 0.05 and d_pulgar_anular < 0.05 and d_pulgar_menique < 0.05):
        return "O"  # Letra O (todos los dedos cerrados)
    
    elif (d_indice_base <0.1 and d_medio_base <0.1 and d_anular_base <0.1 and d_menique_base <0.1) and d_pulgar_indice<0.15 and d_indice_medio<0.1  :
        return "E"  
    
    elif (d_pulgar_indice <0.11 and d_pulgar_medio > 0.15 and d_pulgar_anular > 0.2 and d_pulgar_menique > 0.2):
        return "X"
    
    
    
    elif (d_pulgar_indice > 0.1 and d_pulgar_medio > 0.1 and d_pulgar_anular < 0.05 and d_pulgar_menique < 0.05):
        return "4"  # Número 4 (índice y medio levantados)
    
    elif (d_pulgar_indice < 0.05 and d_pulgar_medio < 0.05 and d_pulgar_anular > 0.1 and d_pulgar_menique > 0.1):
        return "36"  # Número 36 (anular y meñique levantados)
    
    elif (d_pulgar_indice > 0.1 and d_pulgar_medio < 0.05 and d_pulgar_anular > 0.1 and d_pulgar_menique < 0.05):
        return "59"  # Número 59 (índice y anular levantados)
    
    elif (d_pulgar_indice < 0.05 and d_pulgar_medio < 0.05 and d_pulgar_anular < 0.05 and d_pulgar_menique < 0.05 and distancia(pulgar_tip, palma_base) < 0.1):
        return "Comida"  # Puño cerrado (gesto de comer)
    
    else:
        return "No detectado"

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesto = detectar_gesto(hand_landmarks)
            cv2.putText(frame, f"Gesto: {gesto}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Deteccion de Gestos LSM", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
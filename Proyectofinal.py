import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
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

    # Bases de los dedos 
    base_indice = landmarks.landmark[5]
    base_medio = landmarks.landmark[9]
    base_anular = landmarks.landmark[13]
    base_menique = landmarks.landmark[17]
    base_pulgar = landmarks.landmark[2]

    # Distancias
    d_pulgar_baseindice = distancia(pulgar_tip, base_indice)
    d_pulgar_indice = distancia(pulgar_tip, indice_tip)
    d_pulgar_medio = distancia(pulgar_tip, medio_tip)
    d_pulgar_anular = distancia(pulgar_tip, anular_tip)
    d_pulgar_menique = distancia(pulgar_tip, menique_tip)
    d_indice_medio = distancia(indice_tip, medio_tip)
    d_indice_base = distancia(indice_tip, base_indice)
    d_baseanular_pulgar = distancia(base_anular, pulgar_tip)
    d_medio_base = distancia(medio_tip, base_medio)
    d_anular_base = distancia(anular_tip, base_anular)
    d_menique_base = distancia(menique_tip, base_menique)
    d_anular_menique = distancia(anular_tip, menique_tip)
    d_pulgar_base = distancia(pulgar_tip, base_pulgar)

    # Gestos
    if (d_pulgar_indice < 0.05 and d_pulgar_medio < 0.05 and d_pulgar_anular < 0.05 and d_pulgar_menique < 0.05):
        return "O"
    elif (d_indice_base < 0.06 and d_medio_base < 0.06 and d_anular_base < 0.06 and d_menique_base < 0.06) and d_pulgar_indice < 0.15 and d_indice_medio < 0.1:
        return "E"
    elif (d_pulgar_indice < 0.11 and d_pulgar_medio > 0.15 and d_pulgar_anular > 0.2 and d_pulgar_menique > 0.2 and d_menique_base < 0.1):
        return "X"
    elif (d_indice_base > 0.16 and d_medio_base > 0.16 and d_anular_base > 0.16 and d_menique_base > 0.16 and d_baseanular_pulgar < 0.1):
        return "4"
    elif (d_pulgar_medio < 0.05 and d_anular_menique < 0.6 and d_indice_base > 0.16):
        return "30"
    elif (d_indice_base > 0.15 and d_medio_base > 0.15 and d_anular_base > 0.15 and d_pulgar_menique < 0.05 and d_pulgar_medio > 0.2):
        return "6"
    elif (d_pulgar_indice < 0.05 and d_menique_base > 0.18 and d_anular_base > 0.25 and d_medio_base > 0.18):
        return "9"
    elif (d_pulgar_base > 0.13 and d_indice_base > 0.16 and d_medio_base > 0.16 and d_anular_base > 0.16 and d_menique_base > 0.16):
        return "50"
    elif (d_pulgar_indice < 0.1 and d_pulgar_medio < 0.1 and d_pulgar_anular < 0.1 and d_pulgar_menique < 0.1 and d_medio_base > 0.12):
        return "Comida"
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

    gestos = {"Left": None, "Right": None}

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            etiqueta_mano = handedness.classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesto = detectar_gesto(hand_landmarks)
            gestos[etiqueta_mano] = gesto

        gesto_izq = gestos["Left"] if gestos["Left"] else ""
        gesto_der = gestos["Right"] if gestos["Right"] else ""

        if (gesto_izq == "30" and gesto_der == "6") or (gesto_izq == "6" and gesto_der == "30"):
            gesto_completo = "36"
        elif (gesto_izq == "50" and gesto_der == "9") or (gesto_izq == "9" and gesto_der == "50"):
            gesto_completo = "59"
        else:
            gesto_completo = f"{gesto_izq}{gesto_der}"

        # Mostrar solo si alguno fue detectado
        if gesto_completo.strip():
            cv2.putText(frame, f" {gesto_completo}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    cv2.imshow("Deteccion de Gestos LSM", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


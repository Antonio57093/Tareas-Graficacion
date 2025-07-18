# manos.py

```python
"""
PROGRAMA: Detección y Visualización de Puntos de Mano con MediaPipe
DESCRIPCIÓN:
Este programa emplea la biblioteca MediaPipe para detectar manos en tiempo real desde la cámara. Dibuja los puntos clave (landmarks) de cada mano sobre la imagen usando círculos verdes, facilitando el análisis de gestos o poses.
"""
import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar manos
    results = hands.process(frame_rgb)

    # Dibujar los puntos clave y conexiones
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx,landmark in enumerate (hand_landmarks.landmark):
                h,w,_=frame.shape
                x,y=int(landmark.x*w),int (landmark.y*h)
                cv2.circle(frame,(x,y),2,(12,233,4),-1)
            #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostrar la imagen
    cv2.imshow("Salida", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
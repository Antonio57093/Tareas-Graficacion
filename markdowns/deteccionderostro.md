# deteccionderostro.py

```python
import cv2
import mediapipe as mp

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar dibujador de MediaPipe
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))  # Puntos verdes

drawing_spec_eyes = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 0, 255))  # Puntos rojos para ojos
drawing_spec_lips = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0))  # Puntos azules para labios

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, drawing_spec, drawing_spec)
            
    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_RIGHT_EYE, drawing_spec_eyes, drawing_spec_eyes)
            
     # Dibujar los ojos con un color diferente
    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_LEFT_EYE, drawing_spec_eyes, drawing_spec_eyes)            
    # Dibujar la boca con un color diferente
    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_LIPS, drawing_spec_lips, drawing_spec_lips)
    cv2.imshow("Puntos Faciales - MediaPipe", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
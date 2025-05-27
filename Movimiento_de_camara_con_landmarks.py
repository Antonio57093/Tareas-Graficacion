import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
import sys
import cv2
import mediapipe as mp
import math

# Inicializar MediaPipe y cámara
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)


# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 1.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.4  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas


def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)


def draw_trunk():
    """Dibuja el tronco del árbol como un cilindro"""
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glTranslatef(0.0, 0.0, 0.0)  # Posicionar el tronco
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  # Radio y altura del cilindro
    glPopMatrix()


def draw_foliage():
    """Dibuja las hojas del árbol como una esfera"""
    glPushMatrix()
    glColor3f(0.1, 0.8, 0.1)  # Verde para las hojas
    glTranslatef(0.0, 2.0, 0.0)  # Posicionar las hojas encima del tronco
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)  # Radio de la esfera
    glPopMatrix()


def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para el suelo
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()


def draw_scene():
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Punto al que mira
              camera_up[0], camera_up[1], camera_up[2])  # Vector hacia arriba

    draw_ground()  # Dibuja el suelo
    draw_trunk()   # Dibuja el tronco
    draw_foliage() # Dibuja las hojas

    glfw.swap_buffers(window)


def process_input():
    global camera_pos

    # Capturar frame de la cámara
    ret, frame = cap.read()
    if not ret:
        return

    # Procesar imagen para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        
        # Obtener puntos del pulgar (4) e índice (8)
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        
        # Calcular distancia
        distance = math.sqrt((thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2)

        # Ajustar la cámara en Z según la distancia
        if distance > 0.15:
            camera_pos[2] += camera_speed  # Alejar
        elif distance < 0.08:
            camera_pos[2] -= camera_speed  # Acercar

    # Mostrar la cámara
    cv2.imshow('Camera', frame)
    cv2.waitKey(1)



    # Capturar frame de la cámara
    ret, frame = cap.read()
    if not ret:
        return

    # Procesar imagen para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        
        # Obtener puntos del pulgar (4) e índice (8)
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        
        # Calcular distancia
        distance = math.sqrt((thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2)

        # Ajustar la cámara en Z según la distancia
        if distance > 0.15:
            camera_pos[2] += camera_speed  # Alejar
        elif distance < 0.08:
            camera_pos[2] -= camera_speed  # Acercar



def key_callback(window, key, scancode, action, mods):
    """Actualiza el estado de las teclas"""
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena Completa", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        process_input()  # Procesar teclas presionadas
        draw_scene()
        glfw.poll_events()

    cap.release()
    cv2.destroyAllWindows()

    glfw.terminate()


if __name__ == "__main__":
    main()
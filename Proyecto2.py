import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math
from PIL import Image
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Variables de cámara


camera_pos = [10.0, 5.0, 10.0]
camera_up = [0.0, 1.0, 0.0]
camera_yaw = -135.0
camera_pitch = 0.0
camera_speed = 0.1
camera_front = [0.0, 0.0, -1.0]

# IDs de texturas
texture_ids = {}


def update_camera_front():
    global camera_front
    yaw_rad = math.radians(camera_yaw)
    pitch_rad = math.radians(camera_pitch)
    camera_front = [
        math.cos(pitch_rad) * math.cos(yaw_rad),
        math.sin(pitch_rad),
        math.cos(pitch_rad) * math.sin(yaw_rad)
    ]
    # Normaliza el vector
    norm = math.sqrt(sum(i**2 for i in camera_front))
    camera_front = [i / norm for i in camera_front]


def cargar_textura(archivo):
    img = Image.open(archivo)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return textura_id

def dibujar_pixel(pos_centro, index, color=(0, 1, 0), offset=0.2,
                  cols=4, rows=4, ancho_total=0.25, alto_total=0.25):
    x_c, y_c, z_c = pos_centro
    lado_pixel_x = ancho_total / cols
    lado_pixel_y = alto_total / rows
    index -= 1
    fila = index // cols
    col = index % cols
    x_start = x_c - (ancho_total / 2) + (lado_pixel_x / 2)
    y_start = y_c + (alto_total / 2) - (lado_pixel_y / 2)
    x_pos = x_start + col * lado_pixel_x
    y_pos = y_start - fila * lado_pixel_y
    z_pos = z_c + offset
    # Dibuja el cubito
    glPushMatrix()
    glTranslatef(x_pos, y_pos, z_pos)
    glColor3f(*color)
    half_x = lado_pixel_x / 2
    half_y = lado_pixel_y / 2
    half_z = 0.03125 / 2  # profundidad del cubito
    glBegin(GL_QUADS)
    # frontal
    glVertex3f(-half_x, -half_y,  half_z)
    glVertex3f( half_x, -half_y,  half_z)
    glVertex3f( half_x,  half_y,  half_z)
    glVertex3f(-half_x,  half_y,  half_z)
    # trasera
    glVertex3f(-half_x, -half_y, -half_z)
    glVertex3f(-half_x,  half_y, -half_z)
    glVertex3f( half_x,  half_y, -half_z)
    glVertex3f( half_x, -half_y, -half_z)
    # laterales
    glVertex3f(-half_x, -half_y, -half_z)
    glVertex3f(-half_x, -half_y,  half_z)
    glVertex3f(-half_x,  half_y,  half_z)
    glVertex3f(-half_x,  half_y, -half_z)
    glVertex3f( half_x, -half_y, -half_z)
    glVertex3f( half_x,  half_y, -half_z)
    glVertex3f( half_x,  half_y,  half_z)
    glVertex3f( half_x, -half_y,  half_z)
    # superior
    glVertex3f(-half_x,  half_y, -half_z)
    glVertex3f(-half_x,  half_y,  half_z)
    glVertex3f( half_x,  half_y,  half_z)
    glVertex3f( half_x,  half_y, -half_z)
    # inferior
    glVertex3f(-half_x, -half_y, -half_z)
    glVertex3f( half_x, -half_y, -half_z)
    glVertex3f( half_x, -half_y,  half_z)
    glVertex3f(-half_x, -half_y,  half_z)
    glEnd()
    glPopMatrix()


def dibujar_cuboid(pos=(0, 0, 0), ancho=1.0, alto=1.0, largo=2.0, color=(1.0, 1.0, 0.0), textura=None):
    x, y, z = pos
    w = ancho / 2
    h = alto / 2
    l = largo / 2
    vertices = np.array([
        # Cara frontal
        [-w, -h,  l], [ w, -h,  l], [ w,  h,  l], [-w,  h,  l],
        # Cara trasera
        [-w, -h, -l], [ w, -h, -l], [ w,  h, -l], [-w,  h, -l],
        # Cara izquierda
        [-w, -h, -l], [-w, -h,  l], [-w,  h,  l], [-w,  h, -l],
        # Cara derecha
        [ w, -h, -l], [ w,  h, -l], [ w,  h,  l], [ w, -h,  l],
        # Cara superior
        [-w,  h, -l], [-w,  h,  l], [ w,  h,  l], [ w,  h, -l],
        # Cara inferior
        [-w, -h, -l], [ w, -h, -l], [ w, -h,  l], [-w, -h,  l]
    ], dtype=np.float32)
    normals = np.array([
        [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],  # Frontal
        [0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1], # Trasera
        [-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0], # Izquierda
        [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],    # Derecha
        [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],    # Superior
        [0, -1, 0], [0, -1, 0], [0, -1, 0], [0, -1, 0] # Inferior
    ], dtype=np.float32)
    tex_coords = np.array([
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]
    ], dtype=np.float32)
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    if textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_QUADS)
    for i in range(24):
        if textura:
            glTexCoord2fv(tex_coords[i])
        glNormal3fv(normals[i])
        glVertex3fv(vertices[i])
    glEnd()
    if textura:
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def dibujar_suelo(tamano=20.0, textura=None):
    glPushMatrix()
    if textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(0.5, 0.5, 0.5)
    
    mitad = tamano / 2.0
    repeticiones = tamano / 2.0  # Para que las texturas no se estiren
    
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-mitad, 0.0, -mitad)
    glTexCoord2f(repeticiones, 0.0)
    glVertex3f(mitad, 0.0, -mitad)
    glTexCoord2f(repeticiones, repeticiones)
    glVertex3f(mitad, 0.0, mitad)
    glTexCoord2f(0.0, repeticiones)
    glVertex3f(-mitad, 0.0, mitad)
    glEnd()
    
    if textura:
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def dibujar_cubo(pos=(0, 0, 0), color=(0.0, 1.0, 0.0), textura=None):
    glPushMatrix()
    glTranslatef(*pos)
    glColor3f(*color)
    if textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1.0, 1.0, 1.0)  # Color blanco para no afectar la textura

    cube_size = 0.25
    half_size = cube_size / 2
    glBegin(GL_QUADS)
    # Cara frontal
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size,  half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f( half_size, -half_size,  half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f( half_size,  half_size,  half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size,  half_size,  half_size)
    # Cara trasera
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size,  half_size, -half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f( half_size,  half_size, -half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f( half_size, -half_size, -half_size)
    # Cara izquierda
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size, -half_size,  half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f(-half_size,  half_size,  half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size,  half_size, -half_size)
    # Cara derecha
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f( half_size, -half_size, -half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f( half_size,  half_size, -half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f( half_size,  half_size,  half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f( half_size, -half_size,  half_size)
    # Cara superior
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size,  half_size, -half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size,  half_size,  half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f( half_size,  half_size,  half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f( half_size,  half_size, -half_size)
    # Cara inferior
    if textura: glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    if textura: glTexCoord2f(1.0, 0.0)
    glVertex3f( half_size, -half_size, -half_size)
    if textura: glTexCoord2f(1.0, 1.0)
    glVertex3f( half_size, -half_size,  half_size)
    if textura: glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, -half_size,  half_size)
    glEnd()

    if textura:
        glDisable(GL_TEXTURE_2D)
    
    glPopMatrix()

def creeper(pos_base=(0.0, 0.0, 0.0)):
    x0, y0, z0 = pos_base
    textura_cuerpo = texture_ids.get("piel_creeper")
    
    dibujar_cubo(pos=(x0 + 0.25, y0 + 0.25, z0 + 0.25), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    dibujar_cubo(pos=(x0 + 0.00, y0 + 0.25, z0 + 0.25), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    dibujar_cubo(pos=(x0 + 0.00, y0 + 0.25, z0 - 0.25), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    dibujar_cubo(pos=(x0 + 0.25, y0 + 0.25, z0 - 0.25), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    
    for i in range(3):
        dibujar_cubo(pos=(x0 + 0.00, y0 + 0.50 + i * 0.25, z0), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
        dibujar_cubo(pos=(x0 + 0.25, y0 + 0.50 + i * 0.25, z0), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    
    for dy in [1.25, 1.50]:
        for dx in [0.00, 0.25]:
            for dz in [0.125, -0.125]:
                dibujar_cubo(pos=(x0 + dx, y0 + dy, z0 + dz), color=(0.0, 0.5, 0.0), textura=textura_cuerpo)
    
    cara_izq = (x0 + 0.00, y0 + 1.50, z0 + 0.125)
    cara_der = (x0 + 0.25, y0 + 1.50, z0 + 0.125)
    cara_inf_izq = (x0 + 0.00, y0 + 1.25, z0 + 0.125)
    cara_inf_der = (x0 + 0.25, y0 + 1.25, z0 + 0.125)

    for pos_cara in [cara_izq, cara_der]:
        dibujar_pixel(pos_cara, 14, color=(0, 0, 0.0), offset=0.12)
        dibujar_pixel(pos_cara, 15, color=(0.38, 0.54, 0.318), offset=.12)
        dibujar_pixel(pos_cara, 10, color=(0.38, 0.54, 0.318), offset=0.12)
        dibujar_pixel(pos_cara, 11, color=(0.38, 0.54, 0.318), offset=0.12)
    dibujar_pixel(cara_inf_der, 14, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_der, 10, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_der, 9, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_der, 5, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_izq, 15, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_izq, 11, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_izq, 12, color=(0, 0, 0.0), offset=0.12)
    dibujar_pixel(cara_inf_izq, 8, color=(0, 0, 0.0), offset=0.12)

def golem(pos_base=(0.0, 0.0, 0.0)):
    x0, y0, z0 = pos_base
    textura_cuerpo = texture_ids.get("piel_golem")
    textura_pecho = texture_ids.get("pecho_golem")
    # Pierna derecha 
    dibujar_cuboid(pos=(x0 + 0.28125, y0, z0), ancho=0.375, alto=1.0, largo=0.5, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)
    # Pierna izquierda 
    dibujar_cuboid(pos=(x0 - 0.28125, y0, z0), ancho=0.375, alto=1.0, largo=0.5, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)
    # Cuerpo
    dibujar_cuboid(pos=(x0, y0 + 0.625, z0), ancho=0.5625, alto=0.25, largo=0.6875, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)
    # Pecho 
    pecho_pos = (x0, y0 + 1.125, z0)
    dibujar_cuboid(pos=pecho_pos, ancho=1.125, alto=0.75, largo=0.6875, color=(0.69, 0, 0.616), textura=textura_pecho)
    # Cabeza 
    cabeza_pos = (x0, y0 + 1.8125, z0 + 0.09375)
    dibujar_cuboid(pos=cabeza_pos, ancho=0.5, alto=0.625, largo=0.5, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)
    # Nariz 
    dibujar_cuboid(pos=(x0, y0 + 1.59375, z0 + 0.39375), ancho=0.125, alto=0.25, largo=0.125, color=(1.0, 0.6, 0.4), textura=textura_cuerpo)
    
    # Ojos 
    for idx in [50, 55]:
        dibujar_pixel(
            cabeza_pos, idx, color=(1.0, 0.0, 0.0),
            offset=0.25, cols=8, rows=10, ancho_total=0.5, alto_total=0.625
        )
    for idx in [58, 59, 62, 63]:
        dibujar_pixel(
            cabeza_pos, idx, color=(0.651, 0.553, 0.467),
            offset=0.25, cols=8, rows=10, ancho_total=0.5, alto_total=0.625
        )
    for idx in [201,204,183,186,188,166,167,170,149,152,129,132,134,111,114,115,93,75,55,57,60,37,40,41,42,20,21,22,23,4,5,6]:
        dibujar_pixel(
            pecho_pos, idx, color=(0.341, 0.549, 0.09),
            offset=0.35, cols=18, rows=12, ancho_total=1.125, alto_total=0.75
        )
    for idx in [42, 43, 46, 47, 51, 54]:
        dibujar_pixel(
            cabeza_pos, idx, color=(0.0, 0.0, 0.0),
            offset=0.25, cols=8, rows=10, ancho_total=0.5, alto_total=0.625
        )
    #Brazos
    dibujar_cuboid(pos=(x0 - 0.6875, y0 + 0.5625, z0 + 0.03125), ancho=0.25, alto=1.875, largo=0.375, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)
    dibujar_cuboid(pos=(x0 + 0.6875, y0 + 0.5625, z0 + 0.03125), ancho=0.25, alto=1.875, largo=0.375, color=(0.69, 0.651, 0.616), textura=textura_cuerpo)


def arbol(pos_base=(0.0, 0.0, 0.0)):
    x0, y0, z0 = pos_base
    textura_tronco = texture_ids.get("tronco_arbol")
    textura_hojas = texture_ids.get("hojas_arbol")
    #Tronco
    dibujar_cuboid(
        pos=(x0, y0 + 3.0, z0),  # Centro a 3 bloques de altura
        ancho=1.0, alto=6.0, largo=1.0,
        color=(0.4, 0.3, 0.1),
        textura=textura_tronco
    )
    dibujar_cuboid(
        pos=(x0, y0 + 3.5, z0),  
        ancho=5.0, alto=1.0, largo=5.0,
        color=(0.0, 0.5, 0.0),
        textura=textura_hojas
    )
    dibujar_cuboid(
        pos=(x0, y0 + 4.5, z0),
        ancho=5.0, alto=1.0, largo=5.0,
        color=(0.0, 0.6, 0.0),
        textura=textura_hojas
    )
    dibujar_cuboid(
        pos=(x0, y0 + 5.5, z0),
        ancho=3.0, alto=1.0, largo=3.0,
        color=(0.0, 0.7, 0.0),
        textura=textura_hojas
    )
    altura_extra = y0 + 6.5  
    bloques_extra = [
        (x0, altura_extra, z0 + 1.0),  
        (x0, altura_extra, z0 - 1.0),  
        (x0 + 1.0, altura_extra, z0),  
        (x0 - 1.0, altura_extra, z0)   
    ]
    for pos in bloques_extra:
        dibujar_cuboid(
            pos=pos,
            ancho=1.0, alto=1.0, largo=1.0,
            color=(0.0, 0.7, 0.0),
            textura=textura_hojas
        )
    dibujar_cuboid(
        pos=(x0, altura_extra, z0),
        ancho=1.0, alto=1.0, largo=1.0,
        color=(0.0, 0.8, 0.0),
        textura=textura_hojas
    )


def dibujar_flor(pos_centro, offset=0.01, ancho_total=0.25, alto_total=0.25):
    cols = 7
    rows = 12
    pixeles_rojos = [4, 5, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20,
                     22, 23, 24, 25, 26, 30]

    pixeles_verdes = [31, 32, 39, 46, 53, 60, 64, 65, 67, 69, 70,
                      72, 74, 75, 80, 81, 82]

    for index in pixeles_rojos:
        dibujar_pixel(pos_centro, index, color=(1, 0, 0), offset=offset,
                      cols=cols, rows=rows,
                      ancho_total=ancho_total, alto_total=alto_total)

    for index in pixeles_verdes:
        dibujar_pixel(pos_centro, index, color=(0, 1, 0), offset=offset,
                      cols=cols, rows=rows,
                      ancho_total=ancho_total, alto_total=alto_total)
        


def dibujar_cielo():
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)
    for i in range(0, 100, 2):
        altura = i / 100.0
        color_intensity = 0.7 - (altura * 0.4)
        glColor3f(0.4 * color_intensity, 0.6 * color_intensity, color_intensity)
        
        radio = 50 - (altura * 40)
        for j in range(0, 360, 10):
            rad1 = math.radians(j)
            rad2 = math.radians(j + 10)
            
            glVertex3f(math.cos(rad1) * radio, altura * 20, math.sin(rad1) * radio)
            glVertex3f(math.cos(rad2) * radio, altura * 20, math.sin(rad2) * radio)
            glVertex3f(math.cos(rad2) * (radio - 1), (altura + 0.02) * 20, math.sin(rad2) * (radio - 1))
            glVertex3f(math.cos(rad1) * (radio - 1), (altura + 0.02) * 20, math.sin(rad1) * (radio - 1))
    
    glEnd()
    glEnable(GL_LIGHTING)




def distancia(p1, p2):
    return np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def process_hand_gestures():
    global anular_x_anterior
    global camera_pos, camera_yaw, camera_pitch, hand_y_reference

    ret, frame = cap.read()
    if not ret:
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Puntos clave de los dedos
            landmarks = hand_landmarks
                    
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

            if distancia(pulgar_tip, indice_tip) > 0.20 and d_anular_base < 0.15 and d_menique_base < 0.15 and d_medio_base < 0.15:
                camera_pos[0] += camera_front[0] * camera_speed
                camera_pos[1] += camera_front[1] * camera_speed
                camera_pos[2] += camera_front[2] * camera_speed
                cv2.putText(frame, "ACERCANDO CAMARA", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            if distancia(pulgar_tip, indice_tip) < 0.05 and d_anular_base < 0.15 and d_menique_base < 0.15 and d_medio_base < 0.15:
                camera_pos[0] -= camera_front[0] * camera_speed
                camera_pos[1] -= camera_front[1] * camera_speed
                camera_pos[2] -= camera_front[2] * camera_speed
                cv2.putText(frame, "ALEJANDO CAMARA", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            
            cv2.putText(
                frame, 
                f"Distancia: {d_anular_base:.2f} cm",  # Formato con 2 decimales
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 255),  # Color amarillo (BGR)
                2, 
                cv2.LINE_AA  # Anti-aliasing para mejor visualización
            
            )
            if d_menique_base > 0.20 and d_anular_base<0.15 and d_medio_base<0.15 and d_indice_base<0.15:
                camera_yaw -= camera_speed * 10 
                update_camera_front()  
                cv2.putText(frame, "ROTANDO IZQUIERDA", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            if d_anular_base > 0.20 and d_menique_base<0.15 and d_medio_base<0.15 and d_indice_base<0.15:
                camera_yaw += camera_speed * 10  
                update_camera_front()  
                cv2.putText(frame, "ROTANDO DERECHA", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            if d_medio_base > 0.20:
                camera_pos[1] += camera_speed  # subir cámara
                cv2.putText(frame, "SUBIENDO", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if d_indice_base > 0.20:
                camera_pos[1] -= camera_speed  # bajar cámara
                cv2.putText(frame, "BAJANDO", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



        cv2.imshow('Mano', frame)
        cv2.waitKey(1)
    else:
        hand_y_reference = None



def process_input(window):
    global camera_pos, camera_front, camera_up, camera_yaw
    process_hand_gestures()
    pos = np.array(camera_pos)
    front = np.array(camera_front)
    up = np.array(camera_up)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        pos += camera_speed * front
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        pos -= camera_speed * front
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        right = np.cross(front, up)
        right /= np.linalg.norm(right)
        pos -= camera_speed * right
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        right = np.cross(front, up)
        right /= np.linalg.norm(right)
        pos += camera_speed * right
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        camera_yaw -= 0.5
        update_camera_front()
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        camera_yaw += 0.5
        update_camera_front()
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        pos[1] += camera_speed
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        pos[1] -= camera_speed

    camera_pos[:] = pos.tolist()


def main():
    global camera_pos, camera_front, texture_ids
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
          camera_pos[0] + camera_front[0],
          camera_pos[1] + camera_front[1],
          camera_pos[2] + camera_front[2],
          camera_up[0], camera_up[1], camera_up[2])

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    if not glfw.init():
        return

    glutInit()
    window = glfw.create_window(1200, 800, "Proyecto 2", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    light_pos = [0.0, 20.0, 0.0, 1.0]
    light_diffuse = [0.9, 0.9, 0.7, 1.0]
    light_specular = [1.0, 1.0, 0.9, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    
    # Cargar texturas
    try:
        texture_ids = {
            "piel_creeper": cargar_textura("creeper.png"),
            "piel_golem": cargar_textura("piel.png"),
            "pecho_golem": cargar_textura("pecho.png"),
            "tronco_arbol": cargar_textura("tronco2.png"),
            "hojas_arbol": cargar_textura("hojas2.png"),
            "suelo": cargar_textura("cesped.jpg")
        }
    except Exception as e:
        print(f"Error cargando texturas: {e}")
        texture_ids = {}

    update_camera_front()

    while not glfw.window_should_close(window):
        process_input(window)

        glClearColor(0.53, 0.81, 0.98, 1.0)  # Color de cielo
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = 1200 / 800
        gluPerspective(45, aspect_ratio, 0.1, 200.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        center = np.add(camera_pos, camera_front)
        gluLookAt(*camera_pos, *center, *camera_up)
        dibujar_cielo()
        dibujar_suelo(tamano=50.0, textura=texture_ids.get("suelo"))
  
        arbol(pos_base=(5.0, 0, 3.0))
        arbol(pos_base=(-3.0, 0, -2.0))
        arbol(pos_base=(4.0, 0, -5.0))
        arbol(pos_base=(-8.0, 0, 5.0))
        arbol(pos_base=(10.0, 0, -8.0))
        arbol(pos_base=(10.0, 0, -1.0))
        
        # Flores
        for i in range(20):
            x = math.cos(i * 0.7) * 8 - 5
            z = math.sin(i * 1.2) * 8 + 8
            dibujar_flor((x, 0.15, z))
        
        creeper(pos_base=(3.0, 0.0, 2.0))
        golem(pos_base=(-2.0, 0.52, -3.0))
        creeper(pos_base=(-5.0, 0.0, 5.0))
        golem(pos_base=(6.0, 0.52, -6.0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()
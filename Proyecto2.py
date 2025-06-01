import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math

# Variables de cámara
camera_pos = [10.0, 5.0, 10.0]
camera_up = [0.0, 1.0, 0.0]
camera_yaw = -135.0
camera_speed = 0.01
camera_front = [0.0, 0.0, -1.0]

def update_camera_front():
    global camera_front, camera_yaw
    rad = math.radians(camera_yaw)
    camera_front[0] = math.cos(rad)
    camera_front[2] = math.sin(rad)

from OpenGL.GL import *

def dibujar_cubopequeno_en_cara(base_pos, index, color=(0.0, 1.0, 0.0), offset=0.02):
    """
    Dibuja un cubo pequeño en la cara frontal de un cubo grande.

    base_pos: posición (x,y,z) del centro del cubo grande
    index: posición del cubo pequeño en la subdivisión 4x4 (1 a 16)
           numerado desde la esquina superior izquierda, fila por fila.
    color: color del cubo pequeño
    offset: cuánto sobresale el cubo pequeño en z
    """
    x_c, y_c, z_c = base_pos
    cube_grande_lado = 0.25
    cube_pequeno_lado = cube_grande_lado / 4  # 0.0625

    # Convertir index a fila y columna 0-based
    index_0 = index - 1
    fila = index_0 // 4
    columna = index_0 % 4

    # Calcular posición inicial (esquina superior izquierda) en X e Y
    x_start = x_c - (cube_grande_lado / 2) + (cube_pequeno_lado / 2)
    y_start = y_c + (cube_grande_lado / 2) - (cube_pequeno_lado / 2)

    # Posición final del cubo pequeño:
    x_pos = x_start + columna * cube_pequeno_lado
    y_pos = y_start - fila * cube_pequeno_lado
    z_pos = z_c + offset  # sobresale un poco hacia adelante

    # Ahora dibujamos el cubo pequeño en esa posición
    glPushMatrix()
    glTranslatef(x_pos, y_pos, z_pos)
    glColor3f(*color)
    cube_size = cube_pequeno_lado
    half_size = cube_size / 2

    glBegin(GL_QUADS)
    # Cara frontal
    glVertex3f(-half_size, -half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)

    # Cara trasera
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)

    # Cara izquierda
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size, -half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size, -half_size)

    # Cara derecha
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)

    # Cara superior
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f( half_size,  half_size, -half_size)

    # Cara inferior
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f(-half_size, -half_size,  half_size)
    glEnd()
    glPopMatrix()




def dibujar_rectangulo(pos=(0, 0, 0), ancho=1.0, largo=2.0, color=(1.0, 1.0, 0.0), orientacion="xz"):
    x, y, z = pos
    w = ancho / 2
    l = largo / 2

    glColor3f(*color)
    glBegin(GL_QUADS)

    if orientacion == "xz":
        # En el plano del suelo
        glVertex3f(x - w, y, z - l)
        glVertex3f(x + w, y, z - l)
        glVertex3f(x + w, y, z + l)
        glVertex3f(x - w, y, z + l)

    elif orientacion == "xy":
        # Vertical de frente
        glVertex3f(x - w, y - l, z)
        glVertex3f(x + w, y - l, z)
        glVertex3f(x + w, y + l, z)
        glVertex3f(x - w, y + l, z)

    elif orientacion == "yz":
        # Vertical de lado
        glVertex3f(x, y - l, z - w)
        glVertex3f(x, y - l, z + w)
        glVertex3f(x, y + l, z + w)
        glVertex3f(x, y + l, z - w)

    glEnd()


def dibujar_cubo(pos=(0, 0, 0), color=(0.0, 1.0, 0.0)):
    glPushMatrix()
    glTranslatef(*pos)
    glColor3f(*color)
    cube_size = 0.25
    half_size = cube_size / 2
    glBegin(GL_QUADS)

    # Cara frontal
    glVertex3f(-half_size, -half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)

    # Cara trasera
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)

    # Cara izquierda
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size, -half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size, -half_size)

    # Cara derecha
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)

    # Cara superior
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f( half_size,  half_size, -half_size)

    # Cara inferior
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f(-half_size, -half_size,  half_size)

    glEnd()
    glPopMatrix()


def creeper():
    #Patas
    dibujar_cubo(pos=(9.75, 0.25, 9.75), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.50, 0.25, 9.75), color=(0.0, 0.5, 0.0))

    dibujar_cubo(pos=(9.50, 0.25, 9.25), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 0.25, 9.25), color=(0.0, 0.5, 0.0))

    #Cuerpo
    dibujar_cubo(pos=(9.50, 0.50, 9.50), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 0.50, 9.50), color=(0.0, 0.5, 0.0))

    dibujar_cubo(pos=(9.50, 0.75, 9.50), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 0.75, 9.50), color=(0.0, 0.5, 0.0))

    dibujar_cubo(pos=(9.50, 1, 9.50), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 1, 9.50), color=(0.0, 0.5, 0.0))

    #cabeza
    #PArte inferior de la cabeza
    dibujar_cubo(pos=(9.75, 1.25, 9.625), color=(0.0, 0.5, 0.0))# cara derecha
    dibujar_cubo(pos=(9.50, 1.25, 9.625), color=(0.0, 0.5, 0.0))#cara izquierda
    
    dibujar_cubo(pos=(9.50, 1.25, 9.375), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 1.25, 9.375), color=(0.0, 0.5, 0.0))


    #Parte superior de la cabeza
    dibujar_cubo(pos=(9.75, 1.50, 9.625), color=(0.0, 0.5, 0.0)) # Ojos derecha
    dibujar_cubo(pos=(9.50, 1.50, 9.625), color=(0.0, 0.5, 0.0))# ojo izquierda
    dibujar_cubo(pos=(9.50, 1.50, 9.375), color=(0.0, 0.5, 0.0))
    dibujar_cubo(pos=(9.75, 1.50, 9.375), color=(0.0, 0.5, 0.0))

    #cara
    dibujar_cubopequeno_en_cara((9.75, 1.50, 9.625), 14, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.75, 1.50, 9.625), 15, color=(0.38, 0.54, 0.318), offset=0.1)
    dibujar_cubopequeno_en_cara((9.75, 1.50, 9.625), 10, color=(0.38, 0.54, 0.318), offset=0.1)    
    dibujar_cubopequeno_en_cara((9.75, 1.50, 9.625), 11, color=(0.38, 0.54, 0.318), offset=0.1)    
    
    dibujar_cubopequeno_en_cara((9.50, 1.50, 9.625), 15, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.50, 9.625), 14, color=(0.38, 0.54, 0.318), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.50, 9.625), 10, color=(0.38, 0.54, 0.318), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.50, 9.625), 11, color=(0.38, 0.54, 0.318), offset=0.1)

    dibujar_cubopequeno_en_cara((9.75, 1.25, 9.625), 14, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.75, 1.25, 9.625), 10, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.75, 1.25, 9.625), 9, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.75, 1.25, 9.625), 5, color=(0, 0, 0.0), offset=0.1)

    dibujar_cubopequeno_en_cara((9.50, 1.25, 9.625), 15, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.25, 9.625), 11, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.25, 9.625), 12, color=(0, 0, 0.0), offset=0.1)
    dibujar_cubopequeno_en_cara((9.50, 1.25, 9.625), 8, color=(0, 0, 0.0), offset=0.1)
    



    

def draw_cartesian_grid(size=10, step=0.25):
    glLineWidth(1)
    glColor3f(0.6, 0.6, 0.6)
    glBegin(GL_LINES)

    # Eje X
    for x in np.arange(-size, size + step, step):
        glVertex3f(x, 0, 0)
        glVertex3f(x, 0, 0.05)
    # Eje Z
    for z in np.arange(-size, size + step, step):
        glVertex3f(0, 0, z)
        glVertex3f(0.05, 0, z)
    
    glEnd()

    # Eje X en rojo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-size, 0, 0)
    glVertex3f(size, 0, 0)
    glEnd()
    draw_axis_text((size + 0.5, 0, 0), "X")

    # Eje Z en azul
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, -size)
    glVertex3f(0, 0, size)
    glEnd()
    draw_axis_text((0, 0, size + 0.5), "Z")

    # Coordenadas X
    glColor3f(1.0, 0.0, 0.0)
    for x in np.arange(-size, size + 1, 1):
        draw_text((x, 0.01, 0.1), str(x))

    # Coordenadas Z
    glColor3f(0.0, 0.0, 1.0)
    for z in np.arange(-size, size + 1, 1):
        draw_text((0.1, 0.01, z), str(z))

def draw_text(pos, text):
    glRasterPos3f(*pos)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(ch))

def draw_axis_text(pos, label):
    glRasterPos3f(*pos)
    for ch in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def process_input(window):
    global camera_pos, camera_front, camera_up, camera_yaw

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
    global camera_pos, camera_front

    if not glfw.init():
        return

    glutInit()
    window = glfw.create_window(800, 600, "Plano Cartesiano con Creeper", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    update_camera_front()

    while not glfw.window_should_close(window):
        process_input(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        center = np.add(camera_pos, camera_front)
        gluLookAt(*camera_pos, *center, *camera_up)

        draw_cartesian_grid()
        creeper()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()


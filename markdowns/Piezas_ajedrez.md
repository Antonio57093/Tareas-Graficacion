# Piezas_ajedrez.py

```python
import glfw
from math import cos, sin, pi
from OpenGL.GL import *
from OpenGL.GLU import (
    gluPerspective, gluLookAt,
    gluNewQuadric, gluCylinder,
    gluSphere, gluQuadricNormals,
    GLU_SMOOTH
)
import sys


# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.01
keys = {}

def init():
    """Configuración inicial de OpenGL con iluminación"""
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Iluminación
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_pos = [10.0, 10.0, 10.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    ambient_light = [0.2, 0.2, 0.2, 1.0]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def cilindro(xyz=(0, 0, 0), Ri=0, Rs=0, alt=0, rgb=(0.0, 0.0, 0.0)):
    glPushMatrix()
    glColor3f(*rgb)
    glTranslatef(*xyz)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, Ri, Rs, alt, 16,16)
    glPopMatrix()

def esfera(xyz=(0, 0, 0), radio=1.0, slices=5, stacks=5, rgb=(0.1, 0.0, 0.1)):
    glPushMatrix()
    glColor3f(*rgb)
    glTranslatef(*xyz)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radio, slices, stacks)
    glPopMatrix()


def corona(x, y, z):
    radio_corona = 0.13
    altura_pico = 0.1
    for i in range(6):
        angle = 2 * pi * i / 6
        cx = x + radio_corona * cos(angle)
        cz = z + radio_corona * sin(angle)
        
        glPushMatrix()
        glColor3f(1.0, 1.0, 0.0)  # dorado
        glTranslatef(cx, y, cz)
        glRotatef(-90, 0.09, 0, 0)  # orientar el cono hacia arriba
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluCylinder(quadric, 0.02, 0.0, altura_pico, 16, 16)  # cono
        glPopMatrix()




def dibujarpeon():
    glPushMatrix()
    cilindro((2, 0, 6), 0.2, 0.2, 0.20, (0.0, 0.5, 1.0)) #base del peon
    cilindro((2, 0.2, 6), 0.2, 0.15, 0.30, (0.0, 0.5, 1.0)) #base del peon 2
    cilindro((2, 0.4, 6), 0.163, 0.16, 0.15, (0.2, 0.2, 0.9)) #sobresaliente
    esfera((2, 0.65, 6), 0.17, 32, 32, (0.1, 0.4, 1.0)) #cabeza
    glPopMatrix()

def dibujarrey():
    glPushMatrix()
    
    cilindro((2, 0, 5.5), 0.2, 0.2, 0.20, (0.0, 0.5, 1.0)) #base del rey
    cilindro((2, 0.2,5.5), 0.2, 0.1,0.7, (0.0, 0.5, 1.0)) #base 2
    cilindro((2, 0.63,5.5), 0.13, 0.13, 0.15, (0.2, 0.2, 0.9)) #sobresaliente
    esfera((2, 0.9, 5.5), 0.17, 32, 32, (0.1, 0.4, 1.0)) #cabeza
    cilindro((2,1, 5.5), 0.15, 0.15, 0.09, (1.0, 1.0, 0.0))  # corona dorada
    corona(2, 1.08, 5.5)  # Añade la corona justo encima
    glPopMatrix()

def dibujareina():
    glPushMatrix()
    cilindro((2, 0, 5), 0.2, 0.17, 0.20, (0.0, 0.5, 1.0)) #base
    cilindro((2, 0.2, 5), 0.22, 0.10, 0.35, (0.0, 0.5, 1.0)) #base2
    esfera((2, 0.60, 5), 0.17, 32, 32, (0.0, 0.5, 1.0)) #cuerpo
    cilindro((2, 0.63,5), 0.13, 0.13, 0.15, (0.2, 0.2, 0.9)) #sobresaliente
    esfera((2, 0.9, 5), 0.17, 32, 32, (0.1, 0.4, 1.0)) #cabeza
    
    cilindro((2,1, 5), 0.15, 0.15, 0.09, (1.0, 1.0, 0.0))  # corona dorada
    corona(2, 1.08, 5)  # Añade la corona justo encima
    glPopMatrix()

def dibujarpieza():
    glPushMatrix()
    cilindro((2, 0, 4.5), 0.2, 0.17, 0.20, (0.0, 0.5, 1.0)) #base
    cilindro((2, 0.2,4.5), 0.2, 0.16,0.4, (0.0, 0.5, 1.0)) #base 2
    cilindro((2, 0.53,4.5), 0.17, 0.17, 0.14, (0.2, 0.2, 0.9)) #sobresaliente
    
    esfera((2, 0.76, 4.5), 0.17, 32, 32, (0.1, 0.4, 1.0)) #cabeza
    glPopMatrix()

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])

    draw_ground()
    dibujarpeon()
    dibujarrey()
    dibujareina()
    dibujarpieza()

    glfw.swap_buffers(window)

def process_input():
    global camera_pos
    if keys.get(glfw.KEY_W, False): camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False): camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False): camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False): camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False): camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False): camera_pos[1] -= camera_speed

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

def main():
    global window
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena con Luz", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        process_input()
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

```
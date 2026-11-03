#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 33
punkty = None

def generuj_jajo():
    global punkty
    punkty = np.zeros((N, N, 3))
    u_vals = np.linspace(0.0, 1.0, N)
    v_vals = np.linspace(0.0, 1.0, N)

    for i, u in enumerate(u_vals):
        for j, v in enumerate(v_vals):
            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)
            y = (160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5.0)
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)

            punkty[i, j] = [x, y, z]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)
    generuj_jajo()

def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    #X
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-100.0, 0.0, 0.0)
    glVertex3f(100.0, 0.0, 0.0)

    #Y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -100.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)

    #Z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -100.0)
    glVertex3f(0.0, 0.0, 100.0)
    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / np.pi)
    axes()

    glColor3f(0.5, 0.0, 1.0)
    glPointSize(3.0)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3fv(punkty[i, j])
    glEnd()
    glFlush()

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio,
                -7.5, 7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5,
                -7.5, 7.5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "zad1", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()
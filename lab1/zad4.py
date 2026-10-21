#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.2, 0.2, 0.2, 1.0)

def shutdown():
    pass

def rectangle(x, y, a, b):
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.4, 0)
    glVertex2f(x, y)
    glColor3f(0, 0.8, 0.8)
    glVertex2f(x + a, y)
    glColor3f(0.6, 0.6, 0)
    glVertex2f(x + a, y + b)

    glColor3f(0.5,0,0.5)
    glVertex2f(x, y)
    glColor3f(0, 0.6, 0.6)
    glVertex2f(x + a, y + b)
    glColor3f(0.9, 0.9, 0.9)
    glVertex2f(x, y + b)
    glEnd()

def carpet(x, y, a, b, depth):
    if depth == 0:
        rectangle(x, y, a, b)
    else:
        sub_a = a / 3.0
        sub_b = b / 3.0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1: #srodek pusty
                    continue
                carpet(x + i * sub_a, y + j * sub_b, sub_a, sub_b, depth - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #głębokość rekurencji
    recursion_depth = 2
    carpet(-40, -50, 130, 150, recursion_depth)
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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "zad4", None, None)
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
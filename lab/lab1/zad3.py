#!/usr/bin/env python3
import sys

import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

RANDOMIZE = random.randint(10, 300)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def rectangle(x, y, a, b, d=0.0):
    # x, y - placement, a, b - boki, d - deformacja
    x0 = x + random.uniform(-d, d)
    y0 = y + random.uniform(-d, d)
    x1 = x + a + random.uniform(-d, d)
    y1 = y + random.uniform(-d, d)
    x2 = x + a + random.uniform(-d, d)
    y2 = y + b + random.uniform(-d, d)
    x3 = x + random.uniform(-d, d)
    y3 = y + b + random.uniform(-d, d)

    glBegin(GL_TRIANGLES)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x0, y0)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x1, y1)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x2, y2)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x0, y0)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x2, y2)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x3, y3)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(RANDOMIZE)
    rectangle(-40, -50, 80.0, 100, 15)
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

    window = glfwCreateWindow(400, 400, "zad3", None, None)
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
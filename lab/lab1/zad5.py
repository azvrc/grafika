#!/usr/init/env python3
import sys
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

current_mode = 1

TRI_A = (-70, -50)
TRI_B = (70, -50)
TRI_C = (0, 70)


def generate_chaos_points(num_points=20000):
    random.seed(42)
    px, py = 0, 0
    vertices = [TRI_A, TRI_B, TRI_C]
    points = []
    colors = []

    for _ in range(20):
        v = random.choice(vertices)
        px = (px + v[0]) / 2
        py = (py + v[1]) / 2

    for _ in range(num_points):
        v = random.choice(vertices)
        px = (px + v[0]) / 2
        py = (py + v[1]) / 2
        points.append((px, py))
        colors.append((random.random(), random.random(), random.random()))
    return points, colors


CHAOS_POINTS, CHAOS_COLORS = generate_chaos_points(25000)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    print("Nacisnij '1' - podzial rekurencyjny")
    print("Nacisnij '2' - wyliczanie punktow")


def shutdown():
    pass

def key_callback(window, key, scancode, action, mods):
    global current_mode
    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            current_mode = 1
            print("Aktywny algorytm 1: podzial rekurencyjny")
        elif key == GLFW_KEY_2:
            current_mode = 2
            print("Aktywny algorytm 2: wyliczanie punktow")


def sierpinski_1(ax, ay, bx, by, cx, cy, depth):
    if depth == 0:
        glBegin(GL_TRIANGLES)
        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(ax, ay)
        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(bx, by)
        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(cx, cy)
        glEnd()
    else:
        abx, aby = (ax + bx) / 2, (ay + by) / 2
        bcx, bcy = (bx + cx) / 2, (by + cy) / 2
        cax, cay = (cx + ax) / 2, (cy + ay) / 2

        sierpinski_1(ax, ay, abx, aby, cax, cay, depth - 1)
        sierpinski_1(abx, aby, bx, by, bcx, bcy, depth - 1)
        sierpinski_1(cax, cay, bcx, bcy, cx, cy, depth - 1)


def sierpinski_2():
    glPointSize(1.5)
    glBegin(GL_POINTS)
    for (px, py), (r, g, b) in zip(CHAOS_POINTS, CHAOS_COLORS):
        glColor3f(r, g, b)
        glVertex2f(px, py)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    if current_mode == 1:
        random.seed(100)
        sierpinski_1(TRI_A[0], TRI_A[1], TRI_B[0], TRI_B[1], TRI_C[0], TRI_C[1], depth=3)
    else:
        sierpinski_2()

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "zad5", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
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
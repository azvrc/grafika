#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 25
pkt_orbit = 150
randomajz = np.random.randint(11, 333)
pkt_kula = None

planets = [
    {
        "name": "blu",
        "a": 4.5,
        "e": 0.4,
        "speed": 0.8,
        "phase": 0,
        "color": [0.2, 0.6, 1],
        "radius": 0.45,
        "orbit": None,
        "kolores": None
    },
    {
        "name": "red",
        "a": 6.5,
        "e": 0.25,
        "speed": 0.5,
        "phase": 2.1,
        "color": [1, 0.3, 0.2],
        "radius": 0.6,
        "orbit": None,
        "kolores": None
    },
    {
        "name": "grin",
        "a": 3,
        "e": 0.1,
        "speed": 1.2,
        "phase": 4.2,
        "color": [0.2, 0.8, 0.3],
        "radius": 0.3,
        "orbit": None,
        "kolores": None
    }
]

def generuj_orbity_i_kule():
    global pkt_kula
    pkt_kula = np.zeros((N, N, 3))
    u_vals = np.linspace(0, 1, N)
    v_vals = np.linspace(0, 1, N)

    for i, u in enumerate(u_vals):
        for j, v in enumerate(v_vals):
            #rownania dla kuli
            x = np.sin(np.pi * u) * np.sin(2 * np.pi * v)
            y = np.cos(np.pi * u)
            z = np.sin(np.pi * u) * np.cos(2 * np.pi * v)
            pkt_kula[i, j] = [x, y, z]

    for planet in planets:
        a = planet["a"]
        e = planet["e"]
        p = a * (1 - e ** 2)
        orbit_pts = np.zeros((pkt_orbit, 3))
        theta_vals = np.linspace(0, 2 * np.pi, pkt_orbit)

        for i, theta in enumerate(theta_vals):
            r = p / (1 + e * np.cos(theta))
            x = r * np.cos(theta)
            z = r * np.sin(theta)
            y = 0.0
            orbit_pts[i] = [x, y, z]

        planet["orbit"] = orbit_pts

        #gradient wzdluz v / j
        bazowy = np.array(planet["color"])
        kolores = np.zeros((N, N, 3))
        for i in range(N):
            for j in range(N):
                factor = j / (N - 1)
                kolores[i, j] = bazowy * (0.3 + 0.9 * factor)
        planet["kolores"] = kolores

def startup():
    update_viewport(None, 600, 600)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)
    generuj_orbity_i_kule()

def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    #X
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    #Y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    #Z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

def draw_sun_and_orbits():
    #slonce
    glColor3f(1, 0.8, 0)
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    #orbity
    glLineWidth(1.5)
    for planet in planets:
        glColor3f(0.5, 0, 0.5)
        glBegin(GL_LINE_LOOP)
        for pt in planet["orbit"]:
            glVertex3fv(pt)
        glEnd()

def planety(time):
    for planet in planets:
        #aktualna pozycja planet
        theta_planet = time * planet["speed"] + planet["phase"]
        a = planet["a"]
        e = planet["e"]
        p = a * (1 - e ** 2)
        r = p / (1 + e * np.cos(theta_planet))

        planet_x = r * np.cos(theta_planet)
        planet_z = r * np.sin(theta_planet)
        planet_y = 0.0

        R = planet["radius"]
        kolores_planet = planet["kolores"]

        glPushMatrix()
        glTranslatef(planet_x, planet_y, planet_z)

        #obrot planet wokol wlasnych osi y
        glRotatef(time * 50, 0.0, 1.0, 0.0)

        glBegin(GL_TRIANGLES)
        for i in range(N - 1):
            for j in range(N):
                next_j = (j + 1) % N

                p1 = pkt_kula[i, j] * R
                p2 = pkt_kula[i + 1, j] * R
                p3 = pkt_kula[i, next_j] * R
                p4 = pkt_kula[i + 1, next_j] * R

                c1 = kolores_planet[i, j]
                c2 = kolores_planet[i + 1, j]
                c3 = kolores_planet[i, next_j]
                c4 = kolores_planet[i + 1, next_j]

                glColor3fv(c1)
                glVertex3fv(p1)
                glColor3fv(c2)
                glVertex3fv(p2)
                glColor3fv(c3)
                glVertex3fv(p3)

                glColor3fv(c2)
                glVertex3fv(p2)
                glColor3fv(c4)
                glVertex3fv(p4)
                glColor3fv(c3)
                glVertex3fv(p3)
        glEnd()
        glPopMatrix()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(30, 1, 1, 0)
    axes()
    draw_sun_and_orbits()
    planety(time)
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(600, 600, "zad5", None, None)
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
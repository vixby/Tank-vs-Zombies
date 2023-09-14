from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from math import radians, cos, sin


class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.25
        self.clock = pygame.time.Clock()
        self.clock.tick()

    def update(self):
        delta_time = self.clock.tick()
        self.x += self.speed * cos(radians(self.angle)) * delta_time
        self.y += self.speed * sin(radians(self.angle)) * delta_time

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 0, 0)
        radius = 4

        glVertex2f(0, 0)
        for i in range(0, 360, 5):
            x = radius * cos(radians(i))
            y = radius * sin(radians(i))
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()

    def reflect(self, new_angle):
        self.angle = new_angle

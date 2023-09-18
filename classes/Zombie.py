from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import random
from math import radians, atan2, cos, sin


class Zombie:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed * random.random()
        self.clock = pygame.time.Clock()
        self.clock.tick()

    def draw(self):
        glColor3f(0.0, 0.6, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(self.x - 15, self.y - 10)
        glVertex2f(self.x + 15, self.y - 10)
        glVertex2f(self.x + 15, self.y + 10)
        glVertex2f(self.x - 15, self.y + 10)
        glEnd()

        glColor3f(0.0, 0.3, 0.0)
        glBegin(GL_POLYGON)
        for angle in range(0, 360, 90):
            rads = radians(angle)
            glVertex2f(self.x + 5 + cos(rads) * 3, self.y + 5 + sin(rads) * 3)

        glEnd()

    def update_position(self, tank_position):
        delta_time = self.clock.tick() / 1000
        angle_to_target = atan2(tank_position.y - self.y,
                                tank_position.x - self.x)
        dx = self.speed * cos(angle_to_target) * delta_time
        dy = self.speed * sin(angle_to_target) * delta_time
        self.x += dx
        self.y += dy

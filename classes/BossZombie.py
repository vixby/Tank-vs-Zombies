from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import random
from math import radians, atan2, cos, sin


class BossZombie:
    def __init__(self, x, y, speed=100):
        self.x = x
        self.y = y
        self.speed = speed
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.health = 20

    def draw(self):
        glColor3f(0.0, 0.6, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(self.x - 50, self.y - 20)
        glVertex2f(self.x + 50, self.y - 20)
        glVertex2f(self.x + 50, self.y + 20)
        glVertex2f(self.x - 50, self.y + 20)
        glEnd()

        glColor3f(0.0, 0.3, 0.0)
        glBegin(GL_POLYGON)
        for angle in range(0, 360, 90):
            rads = radians(angle)
            glVertex2f(self.x + 5 + cos(rads) * 3, self.y + 5 + sin(rads) * 3)

        glEnd()

    def update_position(self, target_x, target_y):
        delta_time = self.clock.tick() / 1000
        angle_to_target = atan2(target_y - self.y, target_x - self.x)
        dx = self.speed * cos(angle_to_target) * delta_time
        dy = self.speed * sin(angle_to_target) * delta_time
        self.x += dx
        self.y += dy

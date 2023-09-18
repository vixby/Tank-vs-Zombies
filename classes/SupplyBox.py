from OpenGL.GL import *
from OpenGL.GLU import *
import enum
from classes.Projectile import Projectile
from classes.Shared import Point
from math import cos, sin, radians


class Box(enum.Enum):
    HEALTH = 1
    AMMO = 2
    BOMB = 3


class SupplyBox:
    def __init__(self, position, box_type):
        self.position = position
        self.box_type = box_type
        if self.box_type == Box.HEALTH:
            self.color = (1.0, 0.0, 0.0)
        elif self.box_type == Box.AMMO:
            self.color = (0.6, 0.3, 0.0)
        elif self.box_type == Box.BOMB:
            self.color = (0.0, 0.0, 1.0)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)

        # Draw Box
        glBegin(GL_QUADS)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glVertex2f(0, 0)
        glVertex2f(15, 0)
        glVertex2f(15, 10)
        glVertex2f(0, 10)
        glEnd()

        if self.box_type == Box.HEALTH:
            # White cross for healing box
            glBegin(GL_QUADS)
            glColor3f(1.0, 1.0, 1.0)
            glVertex2f(6, 2)
            glVertex2f(9, 2)
            glVertex2f(9, 8)
            glVertex2f(6, 8)
            glEnd()

            glBegin(GL_QUADS)
            glVertex2f(2, 4)
            glVertex2f(13, 4)
            glVertex2f(13, 6)
            glVertex2f(2, 6)
            glEnd()

        elif self.box_type == Box.AMMO:
            # Draw ammo sign
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 1.0)
            glVertex2f(4, 2)
            glVertex2f(11, 8)
            glVertex2f(11, 2)
            glVertex2f(4, 8)
            glEnd()

        elif self.box_type == Box.BOMB:
            # Draw bomb shape
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1.0, 1.0, 1.0)
            glVertex2f(7.5, 5)
            radius = 3
            for i in range(360):
                x = radius * cos(radians(i)) + 7.5
                y = radius * sin(radians(i)) + 5
                glVertex2f(x, y)
            glEnd()

            # Draw fuse
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 0.0)
            glVertex2f(10, 8)
            glVertex2f(13, 10)
            glEnd()

            # Draw sticker
            glBegin(GL_QUADS)
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(6, 4)
            glVertex2f(9, 4)
            glVertex2f(9, 6)
            glVertex2f(6, 6)
            glEnd()

        glPopMatrix()

    def fire_bomb(self):
        angles = range(0, 360, 10)
        projectiles = []
        for angle in angles:
            new_position = Point(self.position.x, self.position.y)
            new_projectile = Projectile(
                new_position, angle, lifetime=5, color=(0.8, 1.0, 0.0))
            projectiles.append(new_projectile)
        return projectiles

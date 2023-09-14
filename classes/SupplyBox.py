from OpenGL.GL import *
from OpenGL.GLU import *
import enum


class Box(enum.Enum):
    HEALTH = 1
    AMMO = 2


class SupplyBox:
    def __init__(self, x, y, box_type):
        self.x = x
        self.y = y
        self.box_type = box_type
        if self.box_type == Box.HEALTH:
            self.color = (1.0, 0.0, 0.0)
        elif self.box_type == Box.AMMO:
            self.color = (0.0, 0.0, 0.0)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glBegin(GL_QUADS)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glVertex2f(0, 0)
        glVertex2f(15, 0)
        glVertex2f(15, 10)
        glVertex2f(0, 10)
        glEnd()
        glPopMatrix()

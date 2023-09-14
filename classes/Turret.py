from OpenGL.GL import *
from OpenGL.GLU import *
from math import degrees, atan2


class Turret:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self):
        glPushMatrix()  # Save the current transformation matrix
        glRotatef(self.angle, 0, 0, 1)  # Rotate the turret

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.6, 0.6, 0.6)
        glVertex2f(15, 15)
        glVertex2f(15, -15)
        glVertex2f(-15, -15)
        glVertex2f(-15, 15)
        glEnd()

        barrel_width = 3
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(15, -barrel_width / 2)
        glVertex2f(15, barrel_width / 2)
        glVertex2f(45, barrel_width / 2)
        glVertex2f(45, -barrel_width / 2)
        glEnd()

        glPopMatrix()  # Restore the transformation matrix

    def update_angle(self, x_mouse, y_mouse):
        dy = y_mouse - self.y
        dx = x_mouse - self.x
        self.angle = degrees(atan2(dy, dx))

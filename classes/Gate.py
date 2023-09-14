from OpenGL.GL import *
from OpenGL.GLU import *


class Gate:
    def __init__(self, corner_one, corner_two, corner_three, corner_four, corner_five):
        self.corner_one = corner_one
        self.corner_two = corner_two
        self.corner_three = corner_three
        self.corner_four = corner_four
        self.corner_five = corner_five
        self.is_open = False

    def draw(self):
        if not self.is_open:  # Only draw the gate if it is not open
            glPushMatrix()
            glColor3f(0.6, 0.4, 0.2)
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(self.corner_one[0], self.corner_one[1])
            glVertex2f(self.corner_two[0], self.corner_two[1])
            glVertex2f(self.corner_three[0], self.corner_three[1])
            glVertex2f(self.corner_four[0], self.corner_four[1])
            glVertex2f(self.corner_five[0], self.corner_five[1])
            glEnd()
            glPopMatrix()

    def open_gate(self):
        self.is_open = True

    def check_collision(self, x, y):
        min_x = min(self.corner_one[0], self.corner_two[0],
                    self.corner_three[0], self.corner_four[0])
        max_x = max(self.corner_one[0], self.corner_two[0],
                    self.corner_three[0], self.corner_four[0])

        min_y = min(self.corner_one[1], self.corner_two[1],
                    self.corner_three[1], self.corner_four[1])
        max_y = max(self.corner_one[1], self.corner_two[1],
                    self.corner_three[1], self.corner_four[1])

        if min_x <= x <= max_x and min_y <= y <= max_y:
            return True
        else:
            return False

from OpenGL.GL import *
from OpenGL.GLU import *


class Wall:
    def __init__(self, corner_one, corner_two, corner_three, corner_four, corner_five):
        self.corner_one = corner_one
        self.corner_two = corner_two
        self.corner_three = corner_three
        self.corner_four = corner_four
        self.corner_five = corner_five

    def draw_random_lines(self):
        glBegin(GL_LINES)
        glVertex2f(self.x1, self.y1)
        glVertex2f(self.x2, self.y2)
        glEnd()

    def draw(self):
        glPushMatrix()

        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.corner_one[0], self.corner_one[1])
        glVertex2f(self.corner_two[0], self.corner_two[1])
        glVertex2f(self.corner_three[0], self.corner_three[1])
        glVertex2f(self.corner_four[0], self.corner_four[1])
        glVertex2f(self.corner_five[0], self.corner_five[1])
        glEnd()

        glPopMatrix()

    def check_collision(self, x, y):
        if self.corner_one[0] <= x <= self.corner_two[0] and self.corner_one[1] <= y <= self.corner_five[1]:
            return True
        else:
            return False

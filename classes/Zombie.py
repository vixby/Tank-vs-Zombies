from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from classes.Shared import Vector, Point
from math import radians, atan2, cos, sin, degrees
import time


class Zombie:
    def __init__(self, position: Point, speed=5):
        self.position = position
        self.speed = Vector(speed * cos(radians(speed)),
                            speed * sin(radians(speed)))
        self.angle_to_target = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.test = 0
        self.current_time = time.time()
        self.last_reach = self.current_time
        self.reach_interval = 2

    def draw(self):
        self.current_time = time.time()
        flail_amount = sin(self.current_time) * 10

        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.angle_to_target, 0, 0, 1)

        # Draw Body
        glColor3f(0.0, 0.6, 0.0)
        glBegin(GL_POLYGON)
        glVertex2f(-10, -10)
        glVertex2f(8, -9)
        glVertex2f(8, 8)
        glVertex2f(-10, 10)
        glEnd()

        # Draw arms
        glColor3f(0.0, 0.5, 0.0)
        glLineWidth(3)
        glBegin(GL_LINES)

        arm_base_x_left = -7
        arm_base_y_left = -7
        arm_base_x_right = 7
        arm_base_y_right = -7

        if self.current_time - self.last_reach > self.reach_interval:
            glVertex2f(arm_base_x_left, arm_base_y_left)
            glVertex2f(arm_base_x_left - 5, arm_base_y_left +
                       flail_amount)
            glVertex2f(arm_base_x_right, arm_base_y_right)
            glVertex2f(arm_base_x_right + 5, arm_base_y_right -
                       flail_amount)
        else:
            glVertex2f(arm_base_x_left, arm_base_y_left)
            glVertex2f(arm_base_x_left - 5, arm_base_y_left -
                       5 + flail_amount)
            glVertex2f(arm_base_x_right, arm_base_y_right)
            glVertex2f(arm_base_x_right + 5, arm_base_y_right -
                       5 - flail_amount)

        glEnd()

        # Draw Eyes
        glColor3f(1.0, 0.0, 0.0)
        glPointSize(2)
        glBegin(GL_POINTS)
        glVertex2f(2, 2)
        glVertex2f(-2, 2)
        glEnd()
        glLineWidth(2)

        glPopMatrix()

    def update_position(self, tank_position):
        delta_time = self.clock.tick() / 1000
        angle_to_target = atan2(tank_position.y - self.position.y,
                                tank_position.x - self.position.x)

        self.angle_to_target = degrees(angle_to_target) + 90
        # Normalize to [0, 360)
        self.angle_to_target = (self.angle_to_target + 360) % 360

        scalar_speed = 60.0
        dx = scalar_speed * cos(angle_to_target) * delta_time
        dy = scalar_speed * sin(angle_to_target) * delta_time

        self.position.x += dx
        self.position.y += dy

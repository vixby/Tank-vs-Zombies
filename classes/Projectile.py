from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from math import radians, cos, sin
from classes.Shared import Point, Vector
from classes.Wall import Wall


class Projectile:
    def __init__(self, position: Point, angle, lifetime=3, color=(1.0, 0.0, 0.0)):
        self.position = position
        self.motion = Vector(200 * cos(radians(angle)),
                             200 * sin(radians(angle)))
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.lifetime = lifetime
        self.color = color

    def update_position(self):
        delta_time = self.clock.tick() / 1000
        self.lifetime -= delta_time
        dx = self.motion.x * delta_time
        dy = self.motion.y * delta_time
        self.position.x += dx
        self.position.y += dy

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(self.color[0], self.color[1], self.color[2])
        radius = 3

        glVertex2f(0, 0)
        for i in range(0, 360, 5):
            x = radius * cos(radians(i))
            y = radius * sin(radians(i))
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()

    def reflect(self, wall_normal: Vector):
        dot_product = self.motion.dot(wall_normal)
        reflection = self.motion - wall_normal.scale(2 * dot_product)
        self.motion = reflection

    def check_collision_with_wall(self, wall: Wall):
        if wall.is_point_inside_bounding_box(self.position.x, self.position.y):
            if wall.check_collision(self.position.x, self.position.y):
                return True
        return False

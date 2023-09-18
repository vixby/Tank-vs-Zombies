from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from math import radians, cos, sin

from classes.Projectile import Projectile
from classes.Turret import Turret
from classes.Shared import Point, Vector


class PlayerTank:
    def __init__(self, position, color, speed=5, angle=90):
        self.position = position
        self.color = color
        self.health = 20
        # Initialize as a Vector
        self.speed = Vector(speed * cos(radians(angle)),
                            speed * sin(radians(angle)))
        self.turning_left = False
        self.turning_right = False
        self.going_up = False
        self.going_down = False
        self.front_breaking = False
        self.back_breaking = False
        self.angle = angle
        self.max_ammo = 5
        self.ammo = []
        self.turret = Turret(self.position, self.angle)
        self.tracks = []

        self.clock = pygame.time.Clock()

    def rotate_and_translate(self, x, y):
        angle_rad = radians(self.angle)
        new_x = x * cos(angle_rad) - y * sin(angle_rad)
        new_y = x * sin(angle_rad) + y * cos(angle_rad)
        return [new_x + self.position.x, new_y + self.position.y]

    def front_left(self):
        return self.rotate_and_translate(40, 25)

    def front_right(self):
        return self.rotate_and_translate(40, -25)

    def back_left(self):
        return self.rotate_and_translate(-40, 25)

    def back_right(self):
        return self.rotate_and_translate(-40, -25)

    def fire(self):
        barrel_length = 45  # Length of the barrel from your drawing code
        dx = barrel_length * cos(radians(self.turret.angle))
        dy = barrel_length * sin(radians(self.turret.angle))
        if (len(self.ammo) < self.max_ammo):
            new_projectile = Projectile(
                self.position.x + dx, self.position.y + dy, self.turret.angle)
            self.ammo.append(new_projectile)

    def update_position(self):
        delta_time = self.clock.tick() / 1000
        angular_speed = 100

        speed_magnitude = 100
        speed_x = speed_magnitude * cos(radians(self.angle))
        speed_y = speed_magnitude * sin(radians(self.angle))

        if self.going_up and not self.front_breaking:
            self.position.x += speed_x * delta_time
            self.position.y += speed_y * delta_time

        if self.going_down and not self.back_breaking:
            self.position.x -= speed_x * delta_time
            self.position.y -= speed_y * delta_time

        if self.turning_left:
            self.angle += angular_speed * delta_time

        if self.turning_right:
            self.angle -= angular_speed * delta_time

        self.turret.position.x = self.position.x
        self.turret.position.y = self.position.y

    def draw(self):
        glPushMatrix()  # Save the current transformation matrix
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.angle, 0, 0, 1)

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.4, 0.4, 0.4)
        glVertex2f(40, 25)
        glVertex2f(-40, 25)
        glVertex2f(-40, -25)
        glVertex2f(40, -25)
        glEnd()

        glColor3f(0.6, 0.6, 0.6)
        wheel_width = 5
        wheel_height = 10

        for x_offset in [-35, -15, 5, 25]:
            for y_offset in [25, -30]:  # y_offset in the inner loop
                glBegin(GL_TRIANGLE_FAN)
                glVertex2f(x_offset, y_offset)
                glVertex2f(x_offset, y_offset + wheel_width)
                glVertex2f(x_offset + wheel_height, y_offset + wheel_width)
                glVertex2f(x_offset + wheel_height, y_offset)
                glEnd()

        glPopMatrix()  # Restore the transformation matrix

        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        self.turret.draw()
        glPopMatrix()

    def prospective_position(self, dx, dy):
        prospective_fl = [self.front_left()[0] + dx, self.front_left()[1] + dy]
        prospective_fr = [self.front_right()[0] + dx,
                          self.front_right()[1] + dy]
        prospective_bl = [self.back_left()[0] + dx, self.back_left()[1] + dy]
        prospective_br = [self.back_right()[0] + dx, self.back_right()[1] + dy]
        return prospective_fl, prospective_fr, prospective_bl, prospective_br

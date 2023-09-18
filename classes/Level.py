from OpenGL.GL import *
from OpenGL.GLU import *
import pygame


class Level:
    def __init__(self, level, walls, gates, kill_requirement, spawn_rate, tank_positioon, angle, zombie_speed):
        self.walls = walls
        self.gates = gates
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.level = level
        self.kill_requirement = kill_requirement
        self.spawn_rate = spawn_rate
        self.zombie_speed = zombie_speed
        self.tank_position = tank_positioon
        self.angle = angle

    def draw(self):
        for wall in self.walls:
            wall.draw()

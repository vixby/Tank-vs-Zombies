from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from classes.Wall import Wall


class Level:
    def __init__(self, level, kill_requirement, spawn_rate, tank_spawn, angle, zombie_speed):

        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.level = level
        self.kill_requirement = kill_requirement
        self.spawn_rate = spawn_rate
        self.zombie_speed = zombie_speed
        self.tank_spawn = tank_spawn
        self.angle = angle
        self.walls = [
            Wall((0, 0), (0, 40), (800, 40), (800, 0), (0, 0)),
            Wall((0, 600), (0, 590), (800, 590), (800, 600), (0, 600)),
            Wall((0, 0), (10, 0), (10, 600), (0, 600), (0, 0)),
            Wall((800, 0), (790, 0), (790, 600), (800, 600), (800, 0)),
            Wall((0, 0), (100, 0), (50, 30), (0, 100), (0, 0)),
            Wall((800, 0), (700, 0), (750, 30), (800, 100), (800, 0)),
            Wall((0, 600), (100, 600), (50, 570), (0, 500), (0, 600)),
            Wall((800, 600), (700, 600), (750, 570), (800, 500), (800, 600)),
        ]
        if self.level == "1":
            self.walls.append(
                Wall((50, 150), (50, 75), (100, 50), (150, 75), (50, 150)))
        if self.level == "2":
            self.walls.append(
                Wall((50, 150), (50, 75), (100, 50), (150, 75), (50, 150)))
            self.walls.append(
                Wall((750, 450), (750, 525), (700, 550), (650, 525), (750, 450)))
        if self.level == "3":
            self.walls.append(
                Wall((50, 150), (50, 75), (100, 50), (150, 75), (50, 150)))
            self.walls.append(
                Wall((750, 450), (750, 525), (700, 550), (650, 525), (750, 450)))
            self.walls.append(
                Wall((50, 450), (50, 525), (100, 550), (150, 525), (50, 450)))
        if self.level == "4" or self.level == "5":
            self.walls.append(
                Wall((50, 150), (50, 75), (100, 50), (150, 75), (50, 150)))
            self.walls.append(
                Wall((750, 450), (750, 525), (700, 550), (650, 525), (750, 450)))
            self.walls.append(
                Wall((50, 450), (50, 525), (100, 550), (150, 525), (50, 450)))
            self.walls.append(
                Wall((750, 150), (750, 75), (700, 50), (650, 75), (750, 150)))

    def draw(self):
        for wall in self.walls:
            wall.draw()

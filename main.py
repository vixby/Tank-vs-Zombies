import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from classes.Game import Game


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 15)
    game = Game({"x": 800, "y": 600}, font)
    game.init_game()

    while True:
        game.game_loop()

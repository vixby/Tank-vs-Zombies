from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from classes.Zombie import Zombie
from classes.BossZombie import BossZombie
from classes.PlayerTank import PlayerTank
from classes.SupplyBox import SupplyBox, Box
from classes.Wall import Wall
import random
import time

from math import radians, cos, sin


class RandomLines:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def draw_random_lines(self):
        glBegin(GL_LINES)
        glVertex2f(self.x1, self.y1)
        glVertex2f(self.x2, self.y2)
        glEnd()


class Game:
    def __init__(self, screen_size, font):
        self.font = font
        self.clock = pygame.time.Clock()
        self.clock.tick()

        # screen settings
        self.screen_size = screen_size
        self.background_red = 0.1
        self.background_green = 0.1
        self.background_blue = 0.1

        # tank settings
        self.player_tank = PlayerTank(400, 300, (0.5, 0.4, 1.0), speed=100)

        # zombie settings
        self.spawn_interval = 3
        self.last_spawn_time = 0
        self.max_zombies = 25
        self.zombies = []
        self.zombie_kills = 0

        # boss zombie settings
        self.boss_zombie = None

        # supply box settings
        self.health_box_interval = 60
        self.ammo_box_interval = 30
        self.last_health_time = 0
        self.last_ammo_time = 0
        self.boxes = []

        # random walls settings
        self.walls = []
        for _ in range(5):
            x1, y1 = random.randint(0, 200), random.randint(0, 600)
            x2, y2 = random.randint(0, 200), random.randint(0, 600)
            wall = RandomLines(x1, y1, x2, y2)
            self.walls.append(wall)

        self.perimeter_walls = [
            Wall((0, 0), (0, 10), (350, 10), (350, 0), (0, 0)),
            Wall((800, 0), (800, 10), (450, 10), (450, 0), (800, 0)),
            Wall((0, 600), (0, 590), (350, 590), (350, 600), (0, 600)),
            Wall((800, 600), (800, 590), (450, 590), (450, 600), (800, 600)),
            Wall((0, 0), (10, 0), (10, 250), (0, 250), (0, 0)),
            Wall((0, 600), (10, 600), (10, 350), (0, 350), (0, 600)),
            Wall((800, 0), (790, 0), (790, 250), (800, 250), (800, 0)),
            Wall((800, 600), (790, 600), (790, 350), (800, 350), (800, 600)),
        ]

    def draw_health_bar(self):
        for i in range(self.player_tank.health):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1.0, 0.0, 0.0)
            glVertex2f(50 + i * 10, 580)
            glVertex2f(50 + i * 10, 590)
            glVertex2f(60 + i * 10, 590)
            glVertex2f(60 + i * 10, 580)
            glEnd()

    def draw_ammo_count(self):
        for i in range(self.player_tank.max_ammo - len(self.player_tank.ammo)):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(50 + i * 10, 570)
            glVertex2f(50 + i * 10, 580)
            glVertex2f(60 + i * 10, 580)
            glVertex2f(60 + i * 10, 570)
            glEnd()

    def check_tank_collision(self):
        self.player_tank.front_breaking = False
        self.player_tank.back_breaking = False
        dx, dy = self.player_tank.speed * \
            cos(radians(self.player_tank.angle)), self.player_tank.speed * \
            sin(radians(self.player_tank.angle))

        # Calculate prospective corner positions
        prospective_fl = self.player_tank.front_left()
        prospective_fr = self.player_tank.front_right()
        prospective_bl = self.player_tank.back_left()
        prospective_br = self.player_tank.back_right()

        if self.is_out_of_bounds(prospective_fl):
            self.player_tank.front_breaking = True
            self.player_tank.turning_left = False
        elif self.is_out_of_bounds(prospective_fr):
            self.player_tank.front_breaking = True
            self.player_tank.turning_right = False
        elif self.is_out_of_bounds(prospective_bl):
            self.player_tank.back_breaking = True
            self.player_tank.turning_right = False
        elif self.is_out_of_bounds(prospective_br):
            self.player_tank.back_breaking = True
            self.player_tank.turning_left = False
        else:
            self.player_tank.back_breaking = False
            self.player_tank.front_breaking = False

    def is_out_of_bounds(self, position):
        x, y = position
        return x < 11 or x > 789 or y < 11 or y > 589

    def is_counter_clockwise(self, pointA, pointB, pointC):
        return (pointC[1] - pointA[1]) * (pointB[0] - pointA[0]) > (pointB[1] - pointA[1]) * (pointC[0] - pointA[0])

    def do_lines_intersect(self, line1_start, line1_end, line2_start, line2_end):
        return (self.is_counter_clockwise(line1_start, line2_start, line2_end) !=
                self.is_counter_clockwise(line1_end, line2_start, line2_end)) and \
            (self.is_counter_clockwise(line1_start, line1_end, line2_start) !=
                self.is_counter_clockwise(line1_start, line1_end, line2_end))

    def check_supply_hit(self):
        fl, fr, bl, br = self.player_tank.front_left(), self.player_tank.front_right(
        ), self.player_tank.back_left(), self.player_tank.back_right()

        for supply in self.boxes:
            # Create the line segment for the supply box
            supply_point_a = [supply.x - 15, supply.y - 15]
            supply_point_b = [supply.x + 15, supply.y + 15]

            # Check for intersections with each of the four edges of the tank
            if self.do_lines_intersect(fl, fr, supply_point_a, supply_point_b) or \
                    self.do_lines_intersect(fr, br, supply_point_a, supply_point_b) or \
                    self.do_lines_intersect(br, bl, supply_point_a, supply_point_b) or \
                    self.do_lines_intersect(bl, fl, supply_point_a, supply_point_b):
                if supply.box_type == Box.AMMO:
                    self.player_tank.max_ammo += 3
                elif supply.box_type == Box.HEALTH:
                    if self.player_tank.health < 20:
                        self.player_tank.health += 5
                self.boxes.remove(supply)
                return True
        return False

    def circle_collision(x1, y1, r1, x2, y2, r2):
        distance_squared = (x1 - x2)**2 + (y1 - y2)**2
        return distance_squared <= (r1 + r2)**2

    def check_zombie_collision(self):
        fl, fr, bl, br = self.player_tank.front_left(), self.player_tank.front_right(
        ), self.player_tank.back_left(), self.player_tank.back_right()

        for zombie in self.zombies:
            # Create the line segment for the zombie
            zombie_point_a = [zombie.x - 15, zombie.y - 10]
            zombie_point_b = [zombie.x + 15, zombie.y + 10]

            # Check for intersections with each of the four edges of the tank
            if self.do_lines_intersect(fl, fr, zombie_point_a, zombie_point_b) or \
                    self.do_lines_intersect(fr, br, zombie_point_a, zombie_point_b) or \
                    self.do_lines_intersect(br, bl, zombie_point_a, zombie_point_b) or \
                    self.do_lines_intersect(bl, fl, zombie_point_a, zombie_point_b):
                self.player_tank.health -= 1
                self.zombies.remove(zombie)
                return True
        return False

    def check_zombie_hit(self, projectile):
        # Define bounding box for projectile
        projectile_box = [projectile.x - 15, projectile.y -
                          10, projectile.x + 15, projectile.y + 10]

        for zombie in self.zombies:
            # Define bounding box for zombie
            zombie_box = [zombie.x - 5, zombie.y -
                          5, zombie.x + 5, zombie.y + 5]

            # Check for bounding box overlap (Axis-Aligned Bounding Box, AABB)
            if (projectile_box[0] < zombie_box[2] and
                projectile_box[2] > zombie_box[0] and
                projectile_box[1] < zombie_box[3] and
                    projectile_box[3] > zombie_box[1]):

                self.zombies.remove(zombie)
                self.zombie_kills += 1
                return True
        return False

    def check_boss_hit(self, projectile):
        if self.boss_zombie:
            # Define bounding box for projectile
            projectile_box = [projectile.x - 2.5, projectile.y -
                              2.5, projectile.x + 2.5, projectile.y + 2.5]

            # Define bounding box for boss
            boss_box = [self.boss_zombie.x - 50, self.boss_zombie.y -
                        25, self.boss_zombie.x + 50, self.boss_zombie.y + 25]

            # Check for bounding box overlap (Axis-Aligned Bounding Box, AABB)
            if (projectile_box[0] < boss_box[2] and
                projectile_box[2] > boss_box[0] and
                projectile_box[1] < boss_box[3] and
                    projectile_box[3] > boss_box[1]):

                if self.boss_zombie.health == 1:
                    self.boss_zombie = None
                else:
                    self.boss_zombie.health -= 1
                return True
        return False

    def init_game(self):
        pygame.display.init()
        pygame.display.set_mode(
            (self.screen_size["x"], self.screen_size["y"]), DOUBLEBUF | OPENGL)
        glClearColor(self.background_red, self.background_green,
                     self.background_blue, 0.5)

    def game_loop(self):
        if self.boss_zombie:
            print(f"Boss health: {self.boss_zombie.health}")
        self.render_text("Score: " + str(self.zombie_kills), (10, 10))
        self.check_tank_collision()
        if self.check_zombie_collision():
            if self.player_tank.health <= 0:
                self.game_over = True
        current_time = time.time()
        x_mouse, y_mouse = pygame.mouse.get_pos()
        y_mouse = self.screen_size["y"] - y_mouse
        self.player_tank.turret.update_angle(x_mouse, y_mouse)
        self.player_tank.update_position()
        new_ammo = [p for p in self.player_tank.ammo if 0 <=
                    p.x <= 800 and 0 <= p.y <= 600]
        self.player_tank.ammo = new_ammo
        if current_time - self.last_health_time > self.health_box_interval:
            self.spawn_health_box()
            self.last_health_time = current_time
        if current_time - self.last_ammo_time > self.ammo_box_interval:
            self.spawn_ammo_box()
            self.last_ammo_time = current_time
        for supply in self.boxes:
            self.check_supply_hit()
        for projectile in self.player_tank.ammo:
            if self.check_zombie_hit(projectile):
                self.player_tank.ammo.remove(projectile)
            if self.check_boss_hit(projectile):
                self.player_tank.ammo.remove(projectile)
        for zombie in self.zombies:
            zombie.update_position(self.player_tank.x, self.player_tank.y)

        if current_time - self.last_spawn_time > self.spawn_interval and len(self.zombies) < self.max_zombies:
            if self.zombie_kills >= 5 and self.boss_zombie == None:
                self.spawn_boss()
                self.zombies = []
            elif self.zombie_kills % 30 == 0 and self.zombie_kills != 0 and self.zombie_boss == None:
                self.spawn_horde()
            elif not self.boss_zombie:
                self.spawn_zombie()
                self.spawn_zombie()
                self.spawn_zombie()

            self.last_spawn_time = current_time
        for projectile in self.player_tank.ammo:
            projectile.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.player_tank.fire()
        if self.boss_zombie and self.boss_zombie.health > 0:
            self.boss_zombie.update_position(
                self.player_tank.x, self.player_tank.y)

        self.display()

    def draw_walls(self):
        for _ in range(5):
            x1, y1 = random.randint(0, 800), random.randint(0, 600)
            x2, y2 = random.randint(0, 800), random.randint(0, 600)
            wall = Wall(x1, y1, x2, y2)
            self.walls.append(wall)

    def handle_key_down(self, event):
        if event.key == K_LEFT or event.key == K_a:
            self.player_tank.turning_left = True
        elif event.key == K_RIGHT or event.key == K_d:
            self.player_tank.turning_right = True
        elif event.key == K_UP or event.key == K_w:
            self.player_tank.going_up = True
        elif event.key == K_DOWN or event.key == K_s:
            self.player_tank.going_down = True
        elif event.key == K_SPACE:
            self.player_tank.fire()

    def handle_key_up(self, event):
        if event.key == K_LEFT or event.key == K_a:
            self.player_tank.turning_left = False
        elif event.key == K_RIGHT or event.key == K_d:
            self.player_tank.turning_right = False
        elif event.key == K_UP or event.key == K_w:
            self.player_tank.going_up = False
        elif event.key == K_DOWN or event.key == K_s:
            self.player_tank.going_down = False

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, 800, 600)
        gluOrtho2D(0, 800, 0, 600)

        if self.player_tank.health <= 0:
            self.reset_game()
        # if self.is_boss_dead():
        #     self.reset_game()

        self.player_tank.draw()
        for projectile in self.player_tank.ammo:
            projectile.draw()
        for zombie in self.zombies:
            zombie.draw()
        for supply in self.boxes:
            supply.draw()
        self.draw_ammo_count()
        self.draw_health_bar()
        # for wall in self.walls:
        #     wall.draw_random_lines()

        for wall in self.perimeter_walls:
            wall.draw()
        if self.boss_zombie != None:
            self.boss_zombie.draw()

        self.render_text(
            f"Kills until next round: {self.zombie_kills} / 60", (10, 10))
        pygame.display.flip()

    def spawn_boss(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = 400, 600
        elif edge == "bottom":
            x, y = 400, 0
        elif edge == "left":
            x, y = 0, 300
        elif edge == "right":
            x, y = 800, 300

        boss_zombie = BossZombie(x, y)
        self.boss_zombie = boss_zombie

    def spawn_horde(self):
        for _ in range(15):
            self.spawn_zombie()

    def spawn_zombie(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = 400, 600
        elif edge == "bottom":
            x, y = 400, 0
        elif edge == "left":
            x, y = 0, 300
        elif edge == "right":
            x, y = 800, 300

        new_zombie = Zombie(x, y)
        self.zombies.append(new_zombie)

    def spawn_health_box(self):
        x, y = random.randint(50, 750), random.randint(50, 550)
        new_box = SupplyBox(x, y, Box.HEALTH)
        self.boxes.append(new_box)

    def spawn_ammo_box(self):
        x, y = random.randint(50, 750), random.randint(50, 550)
        new_box = SupplyBox(x, y, Box.AMMO)
        self.boxes.append(new_box)

    def reset_game(self):
        self.zombie_kills = 0
        self.player_tank.health = 20
        self.player_tank.max_ammo = 5
        self.player_tank.ammo = []
        self.zombies = []
        self.boxes = []
        self.game_over = False
        self.player_tank.x = 400
        self.player_tank.y = 300

    def render_text(self, text, position, color=(155, 213, 90, 255)):  # Include alpha
        text_surface = self.font.render(text, True, color)

        # Convert to OpenGL texture
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)  # Enable blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blend function

        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glColor4f(1, 1, 1, 1)  # Reset color with alpha

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(position[0], position[1], 0)
        glTexCoord2f(1, 0)
        glVertex3f(position[0]+width, position[1], 0)
        glTexCoord2f(1, 1)
        glVertex3f(position[0]+width, position[1]+height, 0)
        glTexCoord2f(0, 1)
        glVertex3f(position[0], position[1]+height, 0)
        glEnd()

        glDisable(GL_BLEND)  # Disable blending
        glDeleteTextures([texid])
        glDisable(GL_TEXTURE_2D)

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from classes.Zombie import Zombie
from classes.PlayerTank import PlayerTank
from classes.SupplyBox import SupplyBox, Box
from classes.Level import Level
from classes.Shared import Point
from classes.Math import GameMath
import random
import time

levels = [Level('1', kill_requirement=20, spawn_rate=3, tank_spawn=(400, 300), angle=90, zombie_speed=75),
          Level('2', kill_requirement=30, spawn_rate=3,
                tank_spawn=(400, 300), angle=90, zombie_speed=75),
          Level('3', kill_requirement=50, spawn_rate=2,
                tank_spawn=(400, 300), angle=90, zombie_speed=75),
          Level('4', kill_requirement=75, spawn_rate=2,
                tank_spawn=(400, 300), angle=90, zombie_speed=80),
          Level('5', kill_requirement=100, spawn_rate=1, tank_spawn=(400, 300), angle=90, zombie_speed=90)]


class Game:
    def __init__(self, screen_size, font):
        self.game_won = False
        self.game_over = False
        self.font = font
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.current_time = time.time()
        self.game_math = GameMath()

        # screen settings
        self.screen_size = screen_size
        self.background_red = 0.15
        self.background_green = 0.15
        self.background_blue = 0.15

        # level settings
        self.current_level = 0
        self.level = levels[self.current_level]
        self.perimeter_walls = self.level.walls
        self.kill_requirements = self.level.kill_requirement
        self.current_level_index = 0
        self.highest_level_completed = 0

        # tank settings
        self.player_tank = PlayerTank(
            self.level.tank_spawn, (0.4, 0.3, 0.2), self.level.angle)

        # zombie settings
        self.spawn_interval = self.level.spawn_rate
        self.last_spawn_time = self.current_time
        self.max_zombies = 25
        self.zombies = []
        self.zombie_kills = 0
        self.zombie_speed = self.level.zombie_speed

        # supply box settings
        self.health_box_interval = 30
        self.ammo_box_interval = 20
        self.last_health_time = self.current_time
        self.last_ammo_time = self.current_time
        self.last_bomb_time = self.current_time
        self.bomb_box_interval = 25  # <-- Set to low value for aoe special
        self.bomb_ammo = []
        self.boxes = []

        # message settings
        self.message = f"Kills until next round: {self.zombie_kills} / {self.level.kill_requirement}"
        self.message_position = (10, 10)

    def set_level(self, level):

        self.zombies = []
        self.zombie_kills = 0
        self.boxes = []
        self.player_tank.ammo = []
        self.bomb_ammo = []
        self.level = level
        self.current_level = level
        self.perimeter_walls = self.level.walls
        self.kill_requirements = self.level.kill_requirement
        self.spawn_interval = self.level.spawn_rate
        self.player_tank.position = Point(
            self.level.tank_spawn[0], self.level.tank_spawn[1])
        self.player_tank.angle = self.level.angle

    def reset_game(self):
        self.player_tank.health = 10
        self.player_tank.max_ammo = 5
        self.player_tank.position = Point(
            self.level.tank_spawn[0], self.level.tank_spawn[1])
        self.player_tank.angle = self.level.angle
        self.highest_level_completed = 0
        self.current_level_index = 0
        self.level = levels[self.current_level_index]
        self.zombies = []
        self.boxes = []
        self.perimeter_walls = self.level.walls
        self.spawn_interval = self.level.spawn_rate
        self.zombie_kills = 0
        self.kill_requirements = self.level.kill_requirement
        self.game_over = False
        self.game_won = False

    def set_end_of_game(self, message):
        self.zombies = []
        self.boxes = []
        self.perimeter_walls = []
        self.message = message
        self.message_position = (250, 300)

    def game_loop(self):
        if not self.game_won and not self.game_over:
            if self.player_tank.health == 0:
                self.game_over = True
                self.set_end_of_game(
                    "You lost! Press 'R' to restart or 'ESC' to quit.")
            if self.zombie_kills == self.kill_requirements:
                if self.current_level_index == 4:
                    self.game_won = True
                    self.set_end_of_game(
                        "You won! Press 'R' to restart or 'ESC' to quit.")
                self.current_level_index += 1
                if self.current_level_index > self.highest_level_completed and self.game_won == False:
                    self.highest_level_completed = self.current_level_index
                    self.set_level(levels[self.current_level_index])

        self.check_tank_collision()
        self.check_zombie_collision()

        self.current_time = time.time()
        x_mouse, y_mouse = pygame.mouse.get_pos()
        y_mouse = self.screen_size["y"] - y_mouse
        self.player_tank.turret.update_angle(x_mouse, y_mouse)
        self.player_tank.update_position()
        new_ammo = [p for p in self.player_tank.ammo if (
            0 <= p.position.x <= 800 and 0 <= p.position.y <= 600) and p.lifetime > 0]
        self.player_tank.ammo = new_ammo
        for projectile in self.player_tank.ammo:
            projectile.update_position()
        if not self.game_won and not self.game_over:
            self.check_spawning()
            for wall in self.perimeter_walls:
                for p in self.player_tank.ammo:
                    if p.check_collision_with_wall(wall):
                        point1, point2 = wall.get_wall_points(p)
                        wall_normal = wall.calculate_wall_normal(
                            point1, point2)
                        p.reflect(wall_normal)
                for p in self.bomb_ammo:
                    if p.check_collision_with_wall(wall):
                        point1, point2 = wall.get_wall_points(p)
                        wall_normal = wall.calculate_wall_normal(
                            point1, point2)
                        p.reflect(wall_normal)
                    if p.lifetime <= 0:
                        self.bomb_ammo.remove(p)
            for _ in self.boxes:
                self.check_supply_hit()
            for projectile in self.player_tank.ammo:
                if self.check_zombie_hit(projectile):
                    self.player_tank.ammo.remove(projectile)
            for projectile in self.bomb_ammo:
                if self.check_zombie_hit(projectile):
                    self.bomb_ammo.remove(projectile)
            for zombie in self.zombies:
                zombie.update_position(self.player_tank.position)
            for projectile in self.bomb_ammo:
                projectile.update_position()
            self.message = f"Kills until next round: {self.zombie_kills} / {self.level.kill_requirement}"
            self.message_position = (10, 10)
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
        self.display()

    def check_spawning(self):
        if self.current_time - self.last_spawn_time > self.spawn_interval and len(self.zombies) < self.max_zombies:
            for _ in range(random.randint(1, 6)):
                self.spawn_zombie()
            self.last_spawn_time = self.current_time
        if self.current_time - self.last_health_time > self.health_box_interval:
            self.spawn_health_box()
            self.last_health_time = self.current_time
        if self.current_time - self.last_ammo_time > self.ammo_box_interval:
            self.spawn_ammo_box()
            self.last_ammo_time = self.current_time
        if self.current_time - self.last_bomb_time > self.bomb_box_interval:
            self.spawn_bomb_box()
            self.last_bomb_time = self.current_time

    def draw_health_bar(self):
        for i in range(self.player_tank.health):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1.0, 0.0, 0.0)
            glVertex2f(310 + i * 10, 20)
            glVertex2f(310 + i * 10, 40)
            glVertex2f(320 + i * 10, 40)
            glVertex2f(320 + i * 10, 20)
            glEnd()

    def draw_ammo_count(self):
        for i in range(self.player_tank.max_ammo - len(self.player_tank.ammo)):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0.3, 0.6, 0.5)
            glVertex2f(310 + i * 10, 0)
            glVertex2f(310 + i * 10, 20)
            glVertex2f(320 + i * 10, 20)
            glVertex2f(320 + i * 10, 0)
            glEnd()

    def render_info_text(self):
        self.render_text(f"Level: {self.level.level}/5",
                         (650, 10), (200, 200, 200, 0))
        self.render_text("Health", (255, 22), (200, 200, 200, 0))
        self.render_text("Ammo", (255, 2), (200, 200, 200, 0))

    def check_tank_collision(self):
        self.player_tank.front_breaking = False
        self.player_tank.back_breaking = False

        prospective_fl = self.player_tank.front_left()
        prospective_fr = self.player_tank.front_right()
        prospective_bl = self.player_tank.back_left()
        prospective_br = self.player_tank.back_right()

        for wall in self.perimeter_walls:
            if wall.is_point_inside_wall(prospective_fl):
                self.player_tank.front_breaking = True
                self.player_tank.turning_left = False
            if wall.is_point_inside_wall(prospective_fr):
                self.player_tank.front_breaking = True
                self.player_tank.turning_right = False
            if wall.is_point_inside_wall(prospective_bl):
                self.player_tank.back_breaking = True
                self.player_tank.turning_right = False
            if wall.is_point_inside_wall(prospective_br):
                self.player_tank.back_breaking = True
                self.player_tank.turning_left = False

    def check_supply_hit(self):
        fl, fr, bl, br = self.player_tank.front_left(), self.player_tank.front_right(
        ), self.player_tank.back_left(), self.player_tank.back_right()

        for supply in self.boxes:
            # Create the line segment for the supply box
            supply_point_a = [supply.position.x - 15, supply.position.y - 15]
            supply_point_b = [supply.position.x + 15, supply.position.y + 15]

            # Check for intersections with each of the four edges of the tank
            if self.game_math.do_lines_intersect(fl, fr, supply_point_a, supply_point_b) or \
                    self.game_math.do_lines_intersect(fr, br, supply_point_a, supply_point_b) or \
                    self.game_math.do_lines_intersect(br, bl, supply_point_a, supply_point_b) or \
                    self.game_math.do_lines_intersect(bl, fl, supply_point_a, supply_point_b):
                if supply.box_type == Box.AMMO:
                    self.player_tank.max_ammo += 1
                elif supply.box_type == Box.HEALTH:
                    if self.player_tank.health < 20:
                        self.player_tank.health += 5
                elif supply.box_type == Box.BOMB:
                    projectiles = supply.fire_bomb()
                    for projectile in projectiles:
                        self.bomb_ammo.append(projectile)
                self.boxes.remove(supply)
                return True
        return False

    def check_zombie_collision(self):
        fl, fr, bl, br = self.player_tank.front_left(), self.player_tank.front_right(
        ), self.player_tank.back_left(), self.player_tank.back_right()

        for zombie in self.zombies:
            # Create the line segment for the zombie
            zombie_point_a = [zombie.position.x - 15, zombie.position.y - 10]
            zombie_point_b = [zombie.position.x + 15, zombie.position.y + 10]

            # Check for intersections with each of the four edges of the tank
            if self.game_math.do_lines_intersect(fl, fr, zombie_point_a, zombie_point_b) or \
                    self.game_math.do_lines_intersect(fr, br, zombie_point_a, zombie_point_b) or \
                    self.game_math.do_lines_intersect(br, bl, zombie_point_a, zombie_point_b) or \
                    self.game_math.do_lines_intersect(bl, fl, zombie_point_a, zombie_point_b):
                self.player_tank.health -= 1
                self.zombie_kills += 1
                self.zombies.remove(zombie)
                return True
        return False

    def check_zombie_hit(self, projectile):
        projectile_box = [projectile.position.x - 15, projectile.position.y -
                          10, projectile.position.x + 15, projectile.position.y + 10]

        for zombie in self.zombies:
            zombie_box = [zombie.position.x - 5, zombie.position.y -
                          5, zombie.position.x + 5, zombie.position.y + 5]

            if (projectile_box[0] < zombie_box[2] and
                projectile_box[2] > zombie_box[0] and
                projectile_box[1] < zombie_box[3] and
                    projectile_box[3] > zombie_box[1]):

                self.zombies.remove(zombie)
                self.zombie_kills += 1
                return True
        return False

    def init_game(self):
        pygame.display.init()
        pygame.display.set_mode(
            (self.screen_size["x"], self.screen_size["y"]), DOUBLEBUF | OPENGL)
        glClearColor(self.background_red, self.background_green,
                     self.background_blue, 0.5)

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
        elif event.key == K_r and (self.game_over or self.game_won):
            self.reset_game()

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

        self.player_tank.draw()
        for projectile in self.player_tank.ammo:
            projectile.draw()
        for projectile in self.bomb_ammo:
            projectile.draw()
        if not self.game_won and not self.game_over:
            for zombie in self.zombies:
                zombie.draw()
            for supply in self.boxes:
                supply.draw()
            for wall in self.perimeter_walls:
                wall.draw()
            self.draw_ammo_count()
            self.draw_health_bar()
        if not self.game_won and not self.game_over:
            self.render_info_text()
        self.render_text(self.message, self.message_position)
        pygame.display.flip()

    def get_random_position(self):
        zombie_spawn_points = [
            Point(random.randint(50, 750), 550),
            Point(random.randint(50, 750), 50),
            Point(50, random.randint(50, 550)),
            Point(750, random.randint(50, 550)),
        ]
        return zombie_spawn_points[random.randint(0, 3)]

    def spawn_zombie(self):
        spawn = self.get_random_position()
        new_zombie = Zombie(spawn, self.zombie_speed)
        self.zombies.append(new_zombie)

    def spawn_health_box(self):
        new_box = SupplyBox(Point(random.randint(100, 650),
                            random.randint(100, 500)), Box.HEALTH)
        self.boxes.append(new_box)

    def spawn_ammo_box(self):
        new_box = SupplyBox(Point(random.randint(100, 650),
                            random.randint(100, 500)), Box.AMMO)
        self.boxes.append(new_box)

    def spawn_bomb_box(self):
        new_box = SupplyBox(Point(random.randint(100, 650),
                            random.randint(100, 500)), Box.BOMB)
        self.boxes.append(new_box)

    def render_text(self, text, position, color=(255, 213, 150, 50)):
        text_surface = self.font.render(text, True, color)

        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glColor4f(1, 1, 1, 1)

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

        glDisable(GL_BLEND)
        glDeleteTextures([texid])
        glDisable(GL_TEXTURE_2D)

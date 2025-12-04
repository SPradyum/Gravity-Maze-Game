import pygame
from pygame.math import Vector2

from objects import Player, Platform, Enemy, Spike, PowerUp, ExitPortal, neon_rect
from effects import spawn_particles, update_and_draw_particles, draw_grid

BG = (2, 9, 22)
NEON = (0, 255, 255)
TEXT_COLOR = (230, 230, 230)


class LevelManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.W, self.H = width, height

        self.player = Player(80, 80)
        self.gravity = Vector2(0, 1.1)   # default downward gravity

        self.particles = []
        self.walls = []
        self.spikes = []
        self.platforms = []
        self.enemies = []
        self.powerups = []
        self.exit_portal = None

        self.font_small = pygame.font.SysFont("consolas", 22)
        self.font_big = pygame.font.SysFont("consolas", 52)

        self.state = "running"   # running, dead, win
        self.level_index = 1

        # level progression (max level accessible)
        self.unlocked_levels = 1

        # slow-motion powerup
        self.slow_factor = 1.0
        self.slow_timer = 0.0

    # ---------------- LEVEL LOADING ---------------- #

    def load_level(self, index: int):
        self.level_index = index
        self.state = "running"

        # clear lists
        self.particles.clear()
        self.walls.clear()
        self.spikes.clear()
        self.platforms.clear()
        self.enemies.clear()
        self.powerups.clear()
        self.exit_portal = None

        self.player.reset()

        # ---------------- LEVEL 1 (Harder Starter) ----------------
        if index == 1:
            self.player.spawn_pos.update(80, 520)
            self.player.reset()

            self.walls = [
                pygame.Rect(0, 0, self.W, 20),
                pygame.Rect(0, self.H - 20, self.W, 20),
                pygame.Rect(0, 0, 20, self.H),
                pygame.Rect(self.W - 20, 0, 20, self.H),

                pygame.Rect(150, 420, 700, 18),
                pygame.Rect(150, 300, 700, 18),
                pygame.Rect(150, 180, 700, 18),
            ]

            self.spikes = [
                Spike(300, 392), Spike(360, 392), Spike(420, 392),
                Spike(500, 392), Spike(525, 392),
                Spike(300, 272), Spike(360, 272), Spike(420, 272),
                Spike(600, 152), Spike(650, 152), Spike(700, 152),
            ]

            self.enemies = [
                Enemy(200, 260, 28, 28, dx=1, dy=0, distance=90, speed=3),
                Enemy(720, 360, 28, 28, dx=-1, dy=0, distance=70, speed=2.5),
            ]

            self.platforms = [
                Platform(250, 500, 120, 16, dx=1, dy=0, distance=2.0),
                Platform(600, 330, 120, 16, dx=-1, dy=0, distance=2.4),
            ]

            self.powerups = [PowerUp(860, 130, "slow")]
            self.exit_portal = ExitPortal(self.W - 140, 60)

        # ---------------- LEVEL 2 (Maze + Timing + Precision) ----------------
        elif index == 2:
            self.player.spawn_pos.update(80, 80)
            self.player.reset()

            self.walls = [
                pygame.Rect(0, 0, self.W, 20),
                pygame.Rect(0, self.H - 20, self.W, 20),
                pygame.Rect(0, 0, 20, self.H),
                pygame.Rect(self.W - 20, 0, 20, self.H),

                pygame.Rect(200, 120, 600, 18),
                pygame.Rect(200, 250, 600, 18),
                pygame.Rect(200, 380, 600, 18),
                pygame.Rect(200, 510, 600, 18),
                pygame.Rect(390, 120, 18, 390),
                pygame.Rect(610, 120, 18, 390),
            ]

            self.spikes = [
                Spike(230, 480), Spike(260, 480), Spike(290, 480),
                Spike(230, 350), Spike(260, 350), Spike(290, 350),
                Spike(640, 480), Spike(670, 480), Spike(700, 480),
                Spike(640, 220), Spike(670, 220), Spike(700, 220),
                Spike(390, 300), Spike(610, 300),
            ]

            self.enemies = [
                Enemy(430, 160, 26, 26, dx=0, dy=1, distance=140, speed=2),
                Enemy(570, 440, 26, 26, dx=0, dy=-1, distance=140, speed=2.3),
            ]

            self.platforms = [
                Platform(480, 320, 120, 16, dx=1, dy=0, distance=2.8),
            ]

            self.powerups = [PowerUp(500, 200, "shield")]
            self.exit_portal = ExitPortal(self.W - 160, self.H - 160)

        # ---------------- LEVEL 3 (Expert Challenge) ----------------
        else:
            self.player.spawn_pos.update(80, 520)
            self.player.reset()

            self.walls = [
                pygame.Rect(0, 0, self.W, 20),
                pygame.Rect(0, self.H - 20, self.W, 20),
                pygame.Rect(0, 0, 20, self.H),
                pygame.Rect(self.W - 20, 0, 20, self.H),

                pygame.Rect(300, 450, 20, 300),
                pygame.Rect(680, 450, 20, 300),
                pygame.Rect(300, 200, 400, 20),
                pygame.Rect(300, 80, 400, 20),
            ]

            self.spikes = [
                Spike(340, 420), Spike(380, 420), Spike(420, 420), Spike(460, 420),
                Spike(600, 420), Spike(560, 420), Spike(520, 420),
                Spike(320, 160), Spike(360, 160), Spike(590, 160),
            ]

            self.enemies = [
                Enemy(340, 250, 26, 26, dx=1, dy=0, distance=160, speed=2.5),
                Enemy(580, 330, 26, 26, dx=-1, dy=0, distance=160, speed=3.5),
            ]

            self.platforms = [
                Platform(320, 300, 140, 16, dx=0, dy=1, distance=2.8),
                Platform(540, 260, 140, 16, dx=0, dy=-1, distance=2.8),
            ]

            self.powerups = [PowerUp(510, 110, "slow")]
            self.exit_portal = ExitPortal(self.W - 140, 60)

        # reset extra state
        self.slow_factor = 1.0
        self.slow_timer = 0.0
        self.player.has_shield = False
        self.player.shield_hits = 0

    # --------------- INPUT HANDLING --------------- #

    def handle_event(self, event):
        # restart after death if R pressed
        if self.state in ("dead", "win"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.player.reset()
                self.state = "running"

    # --------------- GRAVITY SWITCH --------------- #

    def switch_gravity(self, direction: str):
        base = {
            "UP": Vector2(0, -1.1),
            "DOWN": Vector2(0, 1.1),
            "LEFT": Vector2(-1.1, 0),
            "RIGHT": Vector2(1.1, 0),
        }[direction]
        self.gravity = base * self.slow_factor
        spawn_particles(self.particles, self.player.rect.center)

    # --------------- UPDATE LOOP --------------- #

    def update(self, clock):
        dt = clock.get_time() / 1000.0  # for timers only

        # instant input using key polling
        keys = pygame.key.get_pressed()
        if self.state == "running":
            if keys[pygame.K_w]:
                self.switch_gravity("UP")
            elif keys[pygame.K_s]:
                self.switch_gravity("DOWN")
            elif keys[pygame.K_a]:
                self.switch_gravity("LEFT")
            elif keys[pygame.K_d]:
                self.switch_gravity("RIGHT")

        # slow motion timer
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
                # normalise current gravity direction
                if self.gravity.length() != 0:
                    self.gravity = self.gravity.normalize() * 1.1

        if self.state == "running":
            # gravity & physics
            self.player.apply_gravity(self.gravity)

            # update moving platforms & enemies
            for p in self.platforms:
                p.update()
            for e in self.enemies:
                e.update()

            # platforms behave like walls for collision
            colliders = self.walls + [p.rect for p in self.platforms]
            self.player.move_and_collide(colliders)

            # spike collisions
            hit_deadly = False
            for s in self.spikes:
                if self.player.rect.colliderect(s.rect):
                    if self.player.has_shield and self.player.shield_hits > 0:
                        self.player.shield_hits -= 1
                        if self.player.shield_hits <= 0:
                            self.player.has_shield = False
                    else:
                        hit_deadly = True
                        break

            # enemy collisions
            for e in self.enemies:
                if self.player.rect.colliderect(e.rect):
                    if self.player.has_shield and self.player.shield_hits > 0:
                        self.player.shield_hits -= 1
                        if self.player.shield_hits <= 0:
                            self.player.has_shield = False
                    else:
                        hit_deadly = True
                        break

            if hit_deadly:
                self.state = "dead"

            # powerups
            for p in self.powerups[:]:
                if self.player.rect.colliderect(p.rect):
                    if p.kind == "slow":
                        self.slow_factor = 0.4
                        self.slow_timer = 3.0
                        if self.gravity.length() != 0:
                            self.gravity = self.gravity.normalize() * 1.1 * self.slow_factor
                    elif p.kind == "shield":
                        self.player.has_shield = True
                        self.player.shield_hits = 2
                    self.powerups.remove(p)

            # portal / win
            if self.exit_portal and self.player.rect.colliderect(self.exit_portal.rect):
                self.state = "win"
                self.unlocked_levels = max(self.unlocked_levels, self.level_index + 1)

        self.draw_scene()

    # --------------- RENDERING --------------- #

    def draw_scene(self):
        self.screen.fill(BG)
        draw_grid(self.screen, self.W, self.H)

        # walls
        for w in self.walls:
            neon_rect(self.screen, w, NEON, 3)

        # platforms
        for p in self.platforms:
            p.draw(self.screen)

        # spikes
        for s in self.spikes:
            s.draw(self.screen)

        # enemies
        for e in self.enemies:
            e.draw(self.screen)

        # powerups
        for p in self.powerups:
            p.draw(self.screen)

        # portal
        if self.exit_portal:
            self.exit_portal.draw(self.screen)

        # player
        self.player.draw(self.screen)

        # particles
        update_and_draw_particles(self.screen, self.particles)

        # HUD
        hud = self.font_small.render(
            f"Level {self.level_index}  |  Gravity: {self.gravity}  |  Levels Unlocked: {self.unlocked_levels}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(hud, (20, 10))

        if self.player.has_shield:
            shield_txt = self.font_small.render(
                f"Shield hits left: {self.player.shield_hits}", True, (180, 255, 180)
            )
            self.screen.blit(shield_txt, (20, 35))

        # overlays
        if self.state == "dead":
            overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            overlay.fill((200, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            t = self.font_big.render("YOU DIED – Press R", True, (255, 220, 220))
            self.screen.blit(t, (220, 260))

        elif self.state == "win":
            overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            overlay.fill((0, 255, 120, 150))
            self.screen.blit(overlay, (0, 0))
            t = self.font_big.render("LEVEL COMPLETE!", True, (20, 20, 20))
            self.screen.blit(t, (260, 260))

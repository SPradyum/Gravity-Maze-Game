import pygame
import math

NEON = (0, 255, 255)
PLAYER_COLOR = (255, 234, 0)
SPIKE_COLOR = (255, 30, 60)
PORTAL_COLOR = (255, 0, 255)
PLATFORM_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 90, 120)
SLOW_COLOR = (120, 210, 255)
SHIELD_COLOR = (180, 255, 160)


class Player:
    def __init__(self, x, y, size=28):
        self.rect = pygame.Rect(x, y, size, size)
        self.vel = pygame.Vector2(0, 0)
        self.max_speed = 7
        self.spawn_pos = pygame.Vector2(x, y)
        self.has_shield = False
        self.shield_hits = 0

    def reset(self):
        self.rect.topleft = (self.spawn_pos.x, self.spawn_pos.y)
        self.vel.update(0, 0)
        self.has_shield = False
        self.shield_hits = 0

    def apply_gravity(self, gravity_vec):
        self.vel += gravity_vec
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

    def move_and_collide(self, walls):
        # X movement
        self.rect.x += self.vel.x
        for w in walls:
            if self.rect.colliderect(w):
                if self.vel.x > 0:
                    self.rect.right = w.left
                elif self.vel.x < 0:
                    self.rect.left = w.right

        # Y movement
        self.rect.y += self.vel.y
        for w in walls:
            if self.rect.colliderect(w):
                if self.vel.y > 0:
                    self.rect.bottom = w.top
                elif self.vel.y < 0:
                    self.rect.top = w.bottom

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
        if self.has_shield:
            pygame.draw.rect(surface, SHIELD_COLOR, self.rect, 2)


class Platform:
    def __init__(self, x, y, w, h, dx=0, dy=0, distance=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.origin = pygame.Vector2(x, y)
        self.delta = pygame.Vector2(dx, dy)
        self.distance = distance
        self.t = 0

    def update(self):
        if self.distance <= 0:
            return

        self.t += 0.02  # time offset for smooth move
        offset = math.sin(self.t) * self.distance

        self.rect.topleft = (
            self.origin.x + self.delta.x * offset,
            self.origin.y + self.delta.y * offset,
        )

    def draw(self, surf):
        pygame.draw.rect(surf, PLATFORM_COLOR, self.rect, 2)


class Enemy:
    def __init__(self, x, y, w, h, dx=1, dy=0, distance=120, speed=2):
        self.rect = pygame.Rect(x, y, w, h)
        self.origin = pygame.Vector2(x, y)
        self.delta = pygame.Vector2(dx, dy)
        self.distance = distance
        self.speed = speed
        self.t = 0

    def update(self):
        if self.distance <= 0:
            return

        self.t += 0.02 * self.speed
        offset = math.sin(self.t) * self.distance

        self.rect.topleft = (
            self.origin.x + self.delta.x * offset,
            self.origin.y + self.delta.y * offset,
        )

    def draw(self, surf):
        pygame.draw.rect(surf, ENEMY_COLOR, self.rect)


class Spike:
    def __init__(self, x, y, size=30):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surf):
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(surf, SPIKE_COLOR, points)


class PowerUp:
    def __init__(self, x, y, kind="slow"):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.kind = kind

    def draw(self, surf):
        color = SLOW_COLOR if self.kind == "slow" else SHIELD_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=6)


class ExitPortal:
    def __init__(self, x, y, w=60, h=60):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf):
        pygame.draw.rect(surf, PORTAL_COLOR, self.rect, 3)


def neon_rect(surface, rect, color, width=3):
    pygame.draw.rect(surface, color, rect, width)

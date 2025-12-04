import pygame
import random
import math

NEON = (0, 255, 255)

# ---------------- PARTICLE GENERATOR ---------------- #
def spawn_particles(particles_list, center, color=NEON, amount=30):
    cx, cy = center
    for _ in range(amount):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        radius = random.randint(2, 5)
        particles_list.append([cx, cy, vx, vy, radius, color])


def update_and_draw_particles(surface, particles_list):
    for p in particles_list[:]:
        p[0] += p[2]   # Move X
        p[1] += p[3]   # Move Y
        p[4] -= 0.1    # Shrink radius

        if p[4] <= 0:  # Remove when done
            particles_list.remove(p)
            continue

        pygame.draw.circle(surface, p[5], (int(p[0]), int(p[1])), int(p[4]))


# ---------------- GRID BACKGROUND ---------------- #
def draw_grid(surface, width, height):
    for x in range(0, width, 40):
        pygame.draw.line(surface, (0, 50, 70), (x, 0), (x, height), 1)
    for y in range(0, height, 40):
        pygame.draw.line(surface, (0, 50, 70), (0, y), (width, y), 1)

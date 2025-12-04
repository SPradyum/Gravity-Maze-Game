import pygame, sys
from level_manager import LevelManager
from audio import AudioSystem

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Gravity Switch Maze – Sci-Fi Hologram")

BG = (2, 9, 22)

state = "menu"  # menu, level_select, game

font_big = pygame.font.SysFont("consolas", 60)
font_med = pygame.font.SysFont("consolas", 32)
font_small = pygame.font.SysFont("consolas", 22)

level_manager = LevelManager(screen, WIDTH, HEIGHT)
audio = AudioSystem()
audio.play_music("bg_music.mp3")  # Safe even if file missing


def draw_menu():
    screen.fill(BG)
    title = font_big.render("GRAVITY SWITCH MAZE", True, (0,255,255))
    screen.blit(title, (200, 170))

    msg = font_med.render("Press ENTER to Start", True, (220,220,220))
    screen.blit(msg, (350, 260))

    instructions = [
        "CONTROLS:",
        "W / A / S / D — Switch Gravity Direction instantly",
        "Avoid spikes & enemies",
        "Touch portal to finish the level",
        "Powerups: Slow-motion / Shield",
        "Progress unlocks more levels",
        "ESC — Return to previous screen"
    ]
    y = 340
    for line in instructions:
        t = font_small.render(line, True, (170,170,170))
        screen.blit(t, (320, y))
        y += 28


def draw_level_select():
    screen.fill(BG)
    title = font_big.render("LEVEL SELECT", True, (0,255,255))
    screen.blit(title, (330, 100))

    for i in range(1, 4):
        unlocked = i <= level_manager.unlocked_levels
        color = (240,240,240) if unlocked else (120,120,120)
        text = font_med.render(f"{i}. Level {i}", True, color)
        screen.blit(text, (440, 160 + i * 60))

    info = font_small.render("Press 1 / 2 / 3 To Select Level   |   ESC to Back", True, (170,170,170))
    screen.blit(info, (260, 520))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if state == "menu" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                state = "level_select"

        elif state == "level_select":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"

            if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                choose = int(event.unicode)
                if choose <= level_manager.unlocked_levels:
                    level_manager.load_level(choose)
                    state = "game"

        elif state == "game":
            level_manager.handle_event(event)

            if level_manager.state == "win":
                state = "level_select"   # instantly return after win

    if state == "menu":
        draw_menu()
    elif state == "level_select":
        draw_level_select()
    elif state == "game":
        level_manager.update(clock)

    pygame.display.update()
    clock.tick(60)

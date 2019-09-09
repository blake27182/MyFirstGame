import pygame
import sys
import time
import random

pygame.init()

WIDTH = 800
HEIGHT = 800
BACKGROUND = (0, 0, 0)
DIM = (WIDTH, HEIGHT)


class Box:
    def __init__(self, x, y, w, h, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def move_left(self):
        self.x -= 15

    def move_right(self):
        self.x += 15

    def move_down(self, amount):
        self.y += amount

    def get_display_props(self):
        display_props = (self.x, self.y, self.w, self.h)
        return display_props


def collision(box1, box2):
    a1 = (box1.x, box1.y)
    b1 = (box1.x+box1.w, box1.y)
    c1 = (box1.x, box1.y+box1.h)
    d1 = (box1.x+box1.w, box1.y+box1.h)

    a2 = (box2.x, box2.y)
    b2 = (box2.x+box2.w, box2.y)
    c2 = (box2.x, box2.y+box2.h)
    d2 = (box2.x+box2.w, box2.y+box2.h)

    a1_check = a2[0] < a1[0] < b2[0] and a2[1] < a1[1] < c2[1]
    b1_check = a2[0] < b1[0] < b2[0] and a2[1] < b1[1] < c2[1]
    c1_check = a2[0] < c1[0] < b2[0] and a2[1] < c1[1] < c2[1]
    d1_check = a2[0] < d1[0] < b2[0] and a2[1] < d1[1] < c2[1]

    a2_check = a1[0] < a2[0] < b1[0] and a1[1] < a2[1] < c1[1]
    b2_check = a1[0] < b2[0] < b1[0] and a1[1] < b2[1] < c1[1]
    c2_check = a1[0] < c2[0] < b1[0] and a1[1] < c2[1] < c1[1]
    d2_check = a1[0] < d2[0] < b1[0] and a1[1] < d2[1] < c1[1]

    return (a1_check or b1_check or c1_check or d1_check or a2_check
            or b2_check or c2_check or d2_check)


# game setup

window = pygame.display.set_mode(DIM)
game_over = False
player1 = Box(375, 740, 50, 50)
obstacles = []
obs_int = .5
obs_speed = 20
score = 0
score_font = pygame.font.SysFont("Helvetica", 30)

# event loop

since = time.perf_counter()

while not game_over:
    for event in pygame.event.get():        # event handler

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.move_left()
            if event.key == pygame.K_RIGHT:
                player1.move_right()

    # always draw section

    window.fill(BACKGROUND)
    pygame.draw.rect(window, player1.color, player1.get_display_props())
    score_label = score_font.render(f'Score: {score}', 1, (255, 255, 255))
    window.blit(score_label, (WIDTH-100, HEIGHT-40))

    # always change section

    obs_speed = 20 + score
    obs_int = 10 / obs_speed

    # game logic section

    if time.perf_counter() - since > obs_int:
        since = time.perf_counter()
        xpos = random.randint(0, WIDTH-50)
        obstacles.append(Box(xpos, -50, 50, 50, (0, 0, 255)))

    for i, obstacle in enumerate(obstacles):
        obstacle.move_down(obs_speed)
        pygame.draw.rect(window, obstacle.color, obstacle.get_display_props())
        if collision(obstacle, player1):
            game_over = True
        if obstacle.y > HEIGHT:
            del obstacles[i]
            score += 1

    pygame.display.update()

"""
title: pingpong, version: 0.3
author: madetv1280
last change: 02/01/2024
"""

import pygame
from tkinter import messagebox

# initialize
pygame.init()
pygame.font.init()


def config_screen():
    global screen

    screen = pygame.display.set_mode([screen_x, screen_y])
    pygame.display.set_caption(f'PingPong {game_version}')

    # icon
    program_icon = pygame.image.load('icon.png')
    pygame.display.set_icon(program_icon)


clock = pygame.time.Clock()

game_version = 0.3

# screen / window
screen_x = 1280
screen_y = 720
FPS = 120

EXIT = "exit"
COPY = "copy"
GEN = "gen"

config_screen()

# font
my_font = pygame.font.SysFont('Bahnschrift', 60, bold=True)

points = [0, 0]

# color
white = (240, 240, 240)
black = (20, 20, 20)
red = (255, 0, 0)
green = (0, 255, 0)

# player settings
player_speed = 5
player_width = 30
player_height = 200

player_x = 20
player_y = screen_y / 2 - player_height / 2

# enemy settings
enemy_speed = 5
enemy_width = 30
enemy_height = 200

enemy_x = screen_x - 50
enemy_y = screen_y / 2 - enemy_height / 2

# ball settings
ball_x = screen_x / 2
ball_y = screen_y / 2

ball_radius = 20

ball_speed_x = 5
ball_speed_y = 5

NORMAL = 1
AUTO = 2

mode = NORMAL
debug = False


def monologues(type):
    if type == EXIT:
        global run
        response = messagebox.askyesno("Exit Game", "Do you want to exit the game?")
        if response:
            run = False
    if type == COPY:
        messagebox.showinfo("Copyright-Info", "2024 © Daniel Kamin")

    if type == GEN:
        messagebox.showinfo("Controls", "General Controls\nW = UP		S = DOWN\n1 = NORMAL	2 = AUTO\nC = "
                                        "COPYRIGHT     ESC = Exit\n\nDebug Controls\nT+UP = Time Up    T+DOWN = Time "
                                        "Down\nR+UP = Speed UP R+DOWN = Speed Down\nA = LEFT                 D = RIGHT")


def game(mode):
    def game_draw():

        text_surface = my_font.render(f"{points[0]}     {points[1]}", False, white)

        # playing field marked (middle)
        pygame.draw.line(screen, white, (screen_x / 2, 0), (screen_x / 2, screen_y), width=10)

        # player
        pygame.draw.rect(screen, white, pygame.Rect(player_x, player_y, player_width, player_height), border_radius=15)

        # enemy
        pygame.draw.rect(screen, white, pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height), border_radius=15)

        # ball
        pygame.draw.circle(screen, white,(ball_x, ball_y), ball_radius)

        # points (txt)
        screen.blit(text_surface,(screen_x / 2 - text_surface.get_width() / 2, 30))

        if debug:
            debug_font = pygame.font.SysFont('Bahnschrift', 18, bold=True)

            pygame.draw.line(screen, green,
                             (screen_x / 2, 0), (screen_x / 2, screen_y), width=2)

            pygame.draw.line(screen, red,
                             (0, screen_y/2), (screen_x, screen_y/2), width=2)

            # debug coords for objs
            player_coords_text = debug_font.render(f"X: {player_x} | Y: {player_y}", False, red)
            screen.blit(player_coords_text,(player_x, player_y))

            enemy_coords_text = debug_font.render(f"X: {enemy_x} | Y: {enemy_y}", False, red)
            screen.blit(enemy_coords_text, (enemy_x, enemy_y))

            ball_coords_text = debug_font.render(f"X: {ball_x} | Y: {ball_y}", False, red)
            screen.blit(ball_coords_text, (ball_x, ball_y))

            fps_text = debug_font.render(f"Tick: {FPS}", False, red)
            screen.blit(fps_text, (20, 20))

    def game_run(mode=1):
        global player_speed

        # --- KEY CONTROL --- #
        def player_control():
            global player_y

            if k[pygame.K_w]:
                if player_y >= 0:
                    player_y -= player_speed

            if k[pygame.K_s]:
                if player_y <= screen_y - player_height:
                    player_y += player_speed

        if debug:
            global player_x, FPS, player_speed
            if k[pygame.K_a]:
                player_x -= player_speed

            if k[pygame.K_d]:
                player_x += player_speed

            if k[pygame.K_r] and k[pygame.K_UP]:
                player_speed += 0.1

            if k[pygame.K_r] and k[pygame.K_DOWN]:
                player_speed -= 0.1

            if k[pygame.K_t] and k[pygame.K_UP]:
                if not FPS == 4096:
                    FPS += 1

            if k[pygame.K_t] and k[pygame.K_DOWN]:
                if not FPS == 0:
                    FPS -= 1

        # --- BALL CONTROL --- #
        def ball_movement():
            global ball_x, ball_y
            ball_x += ball_speed_x
            ball_y += ball_speed_y

        def ball_collision():
            global ball_speed_y, ball_speed_x, ball_y, ball_x

            # ball collision
            if ball_y >= screen_y - ball_radius or ball_y <= 0 + ball_radius:
                ball_speed_y *= -1

            # player-ball collision
            if (ball_x - ball_radius <= player_x + player_width / 2 <= ball_x - ball_radius
                    and player_y + player_height >= ball_y >= player_y):
                ball_speed_x *= -1

            # enemy-ball collision
            if (ball_x - ball_radius <= enemy_x - enemy_width / 2 <= ball_x - ball_radius
                    and enemy_y + enemy_height >= ball_y >= enemy_y):
                ball_speed_x *= -1

            # reset ball, when outside
            # player gets a point
            if ball_x >= screen_x - ball_radius + 400:
                ball_y = screen_y / 2
                ball_x = screen_x / 2
                points[0] += 1

            # enemy gets a point
            if ball_x <= 0 + ball_radius - 400:
                ball_y = screen_y / 2
                ball_x = screen_x / 2
                points[1] += 1

        def enemy_tracking_ball():
            global enemy_y
            # enemy-ball following
            if enemy_y < ball_y:
                enemy_y += enemy_speed
            if enemy_y + enemy_height > ball_y:
                enemy_y -= enemy_speed

        def player_tracking_ball():
            global player_y
            # enemy-ball following
            if player_y < ball_y:
                player_y += player_speed
            if player_y + player_height > ball_y:
                player_y -= player_speed

        if mode == NORMAL:
            player_control()

        elif mode == AUTO:
            player_tracking_ball()

        ball_movement()
        ball_collision()

        enemy_tracking_ball()

    game_draw()
    game_run(mode)


run = True

monologues("gen")
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            monologues(EXIT)

    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE]:
        monologues(EXIT)

    if k[pygame.K_c]:
        monologues(COPY)

    if k[pygame.K_1]:
        mode = NORMAL

    if k[pygame.K_2]:
        mode = AUTO

    if k[pygame.K_3]:
        if debug:
            debug = False
        else:
            debug = True

    screen.fill(black)

    game(mode)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

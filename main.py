import pygame
import sys
import random

def ball_animation():
    global ball_speed_x, ball_speed_y, orpheus_score, opponent_orpheus_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball.top <= 0:
        ball.top = 0  # Prevent ball from going off-screen
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.bottom >= screen_height:
        ball.bottom = screen_height  # Prevent ball from going off-screen
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Ball collision with left and right walls (scoring)
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        orpheus_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_orpheus_score += 1
        score_time = pygame.time.get_ticks()

    # Ball collision with paddles
    if ball.colliderect(orpheus):
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1

    if ball.colliderect(opponent_orpheus):
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1

def orpheus_animation():
    if orpheus.top <= 0:
        orpheus.top = 0
    if orpheus.bottom >= screen_height:
        orpheus.bottom = screen_height

def opponent_orpheus_ai():
    if opponent_orpheus.top < ball.y:
        opponent_orpheus.top += opponent_orpheus_speed
    if opponent_orpheus.bottom > ball.y:
        opponent_orpheus.bottom -= opponent_orpheus_speed
    if opponent_orpheus.top <= 0:
        opponent_orpheus.top = 0
    if opponent_orpheus.bottom >= screen_height:
        opponent_orpheus.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()

    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 6 * random.choice((1, -1))
        ball_speed_x = 6 * random.choice((1, -1))
        score_time = None

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
orpheus = pygame.Rect(10, screen_height / 2 - 25, 50, 50)
opponent_orpheus = pygame.Rect(screen_width - 60, screen_height / 2 - 25, 50, 50)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Speeds
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
orpheus_speed = 0
opponent_orpheus_speed = 7

# Scores
orpheus_score = 0
opponent_orpheus_score = 0

# Font
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Sounds
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# Images
orpheus_image = pygame.image.load("orpheus.png").convert_alpha()
orpheus_image = pygame.transform.scale(orpheus_image, (50, 50))


opponent_orpheus_image = pygame.image.load("opponent_orpheus.png").convert_alpha()
opponent_orpheus_image = pygame.transform.scale(opponent_orpheus_image, (50, 50))

# Ball reset timer
score_time = True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                orpheus_speed += 7
            if event.key == pygame.K_UP:
                orpheus_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                orpheus_speed -= 7
            if event.key == pygame.K_UP:
                orpheus_speed += 7

    # Update game state
    ball_animation()
    orpheus.y += orpheus_speed
    orpheus_animation()
    opponent_orpheus_ai()

    # Draw everything
    screen.fill(bg_color)
    screen.blit(orpheus_image, orpheus)
    screen.blit(opponent_orpheus_image, opponent_orpheus)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_restart()

    # Display scores
    orpheus_text = game_font.render(f"{orpheus_score}", False, light_grey)
    screen.blit(orpheus_text, (620, 380))

    opponent_orpheus_text = game_font.render(f"{opponent_orpheus_score}", False, light_grey)
    screen.blit(opponent_orpheus_text, (560, 380))

    # Update display
    pygame.display.flip()
    clock.tick(60)

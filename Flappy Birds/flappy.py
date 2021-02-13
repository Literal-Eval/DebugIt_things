#A rip-off of Flappy Birds
#(C) Ravidev Pandey, 2021

import sys
import pygame
import random
import time

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

gravity = 0.25
bird_movement = 0
game_is_active = False
score = 0
high_score = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((322, 614))
pygame.display.set_caption("Flappy Birds")
pygame.display.set_icon(pygame.image.load("assets/image/bluebird-midflap.png"))
clock = pygame.time.Clock()

background = pygame.image.load("assets/image/background-day.png").convert()
background = pygame.transform.scale(background, (322, 614))

floor = pygame.image.load("assets/image/base.png").convert()
floor_x_pos = 0

score_font = pygame.font.Font("assets/04B_19.TTF", 30)
game_font = pygame.font.Font("assets/04B_19.TTF", 22)
copyright_font = pygame.font.Font("assets/04B_19.TTF", 20)

copyright = copyright_font.render("(C) Ravidev Pandey", True, WHITE)
copyright_rect = copyright.get_rect(center = (166, 20))

pipe_collision_words = ["Mind those pipes.", "Ah shit here we go again.", "Sed Lyf"]
ground_collision_words = ["Are you a wormhole nigga?", "Why are we even here?"]
sky_collision_words = ["Wanna be an astronaut?", "Is life all about pain?"]
to_say = ""

flap_sound = pygame.mixer.Sound("assets/sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("assets/sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("assets/sound/sfx_point.wav")

bird_midflap = pygame.image.load("assets/image/bluebird-midflap.png").convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (41, 29))
bird_upflap = pygame.image.load("assets/image/bluebird-upflap.png").convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (41, 29))
bird_downflap = pygame.image.load("assets/image/bluebird-downflap.png").convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (41, 29))

bird_frames = [bird_midflap, bird_downflap, bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center = (50, 307))

pipe = pygame.image.load("assets/image/pipe-green.png").convert()
pipe = pygame.transform.scale(pipe, (63, 384))
pipe_list = []
pipe_height = [310, 350, 420, 460, 400, 270, 250]

game_over = pygame.image.load("assets/image/message.png").convert_alpha()
game_over = pygame.transform.scale(game_over, (221, 320))
game_over_rect = game_over.get_rect(center = (166, 307))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

SPAWNPIPE = pygame.USEREVENT    
pygame.time.set_timer(SPAWNPIPE, 1200)

def spawn_pipe():

    global pipe_list

    height = pipe_height[random.randint(0, len(pipe_height) - 1)]
    
    pipe_rect_top = pipe.get_rect(midtop = (500, height))
    pipe_rect_bottom = pipe.get_rect(midbottom = (500, height - 100))

    pipe_list.extend([pipe_rect_top, pipe_rect_bottom])

    if len(pipe_list) > 6:
        pipe_list.pop(0)
        pipe_list.pop(0)

def draw_pipe():

    global pipe_list

    for pipe_element in pipe_list:

        pipe_element.centerx -= 5

        if pipe_element.bottom > 614:
            screen.blit(pipe, pipe_element)
        else:
            new_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(new_pipe, pipe_element)

def draw_floor():

    global floor_x_pos

    screen.blit(floor, (floor_x_pos, 535))
    screen.blit(floor, (floor_x_pos + 336, 535))

    floor_x_pos -= 1

    if floor_x_pos <= -336:
        floor_x_pos = 0

def draw_bird():

    global bird_movement, bird, bird_rect

    bird = bird_frames[bird_index]
    bird_rect = bird.get_rect(center = (50, bird_rect.centery))

    bird_movement += gravity
    bird_rect.centery += bird_movement

    rotated_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    screen.blit(rotated_bird, bird_rect)

def draw_score():

    global score, high_score, to_say

    if score > high_score:
        high_score = score
    
    if game_is_active:
        for pipe in pipe_list:
            if pipe.centerx in range(101, 106):
                score += 1
                score_sound.play()
    
    score_text = score_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center = (166, 100))

    screen.blit(score_text, score_rect)

    if not game_is_active:

        high_score_text = score_font.render(f'High score: {high_score}', True, WHITE)
        high_score_rect = high_score_text.get_rect(center = (166, 500))

        to_say_text = game_font.render(to_say, True, BLACK)
        to_say_rect = to_say_text.get_rect(center = (166, 590))

        screen.blit(high_score_text, high_score_rect)
        screen.blit(game_over, game_over_rect)
        screen.blit(to_say_text, to_say_rect)
        screen.blit(copyright, copyright_rect)

def check_collision():

    global game_is_active, pipe_collision_words, sky_collision_words, ground_collision_words
    global to_say

    for pipe in pipe_list:
        if pipe.colliderect(bird_rect):
            game_is_active = False
            random.shuffle(pipe_collision_words)
            to_say = pipe_collision_words[0]
            break
        if bird_rect.top < 0:
            game_is_active = False
            random.shuffle(sky_collision_words)
            to_say = sky_collision_words[0]
            break
        if bird_rect.bottom > 535:
            game_is_active = False
            random.shuffle(ground_collision_words)
            to_say = ground_collision_words[0]
            break
        
    if not game_is_active:
        death_sound.play()

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                if game_is_active:
                    bird_movement = -6
                    flap_sound.play()
                else:
                    bird_movement = 0
                    pipe_list.clear()
                    bird_rect.center = (50, 307)
                    score = 0
                    game_is_active = True
        
        if event.type == BIRDFLAP:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0

        if event.type == SPAWNPIPE:
            if game_is_active:
                spawn_pipe()

    screen.blit(background, (0, 0))
        
    if game_is_active:

        draw_bird()
        draw_pipe()
        check_collision()

    draw_floor()
    draw_score()

    pygame.display.update()

    clock.tick(60)

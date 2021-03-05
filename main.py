import pygame
import sys
import random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 630))
    screen.blit(floor_surface, (floor_x_pos + 500, 630))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(800,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom =(800,random_pipe_pos-250))
    return bottom_pipe,top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=630:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >=630:
        death_sound.play()
        return False
    return True
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement *3,1)
    return new_bird
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (250,90))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 90))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 600))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.init()
screen = pygame.display.set_mode((500 ,720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',35)

#game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/Iubatbg.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface,(500, 720))

floor_surface = pygame.image.load('assets/base.png')
floor_surface = pygame.transform.scale(floor_surface,(500,90))
floor_x_pos = 0

bird_surface = pygame.image.load('assets/angry.png').convert_alpha()
bird_surface = pygame.transform.scale(bird_surface,(50,50))
bird_rect = bird_surface.get_rect(center =(100,350))

pipe_surface = pygame.image.load('assets/unnamed1.png')
pipe_surface = pygame.transform.scale(pipe_surface,(130,460))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1400)
pipe_height = [280,360,460,180]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect( center = (250,350))\

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,350)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    screen.blit(bg_surface,(0,0))

    if game_active:
    #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        score_display('main_game')
        score += 0.009
    #PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -500:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(110)


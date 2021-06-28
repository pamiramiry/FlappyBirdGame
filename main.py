import pygame
import sys
import random


# moves all the pipes to the left
def pipe_move(pipe_l):
    for pipe1 in pipe_l:
        pipe1 .centerx -= 1.1
    return pipe_l


# returns two pipes
def create_pipe():
    y = random.randint(250, 500)
    pipe_down = pipe.get_rect(midtop=(390, y))
    pipe_top = pipe_up.get_rect(midbottom=(390, y-200))
    return pipe_down, pipe_top


# check the newest two pipes and see if the bird collides with it returns false if collision happens
def check_collision(pipe_l):
    alive = True
    if len(pipe_l) > 1:
        if bird_rec.colliderect(pipe_l[len(pipe_l)-1]) or bird_rec.colliderect(pipe_l[len(pipe_l)-2]):
            alive = False
        if bird_rec.centery <= 0 or bird_rec.centery > 575:
            alive = False
    return alive


# displays the message "game over"
def write_game_over():
    screen.blit(game_over, (100, 200))


# writes the score
def write_score():
    score_pic = game_font.render(str(score), True, (255, 255, 255))
    screen.blit(score_pic, (180, 70))


pygame.init()
frame_rate = pygame.time.Clock()

# load up all the images
background = pygame.image.load("sprites/background-night.png")
background = pygame.transform.scale(background, (384, 683))
# Added two ground images to rotate them when one of them reaches the end
ground = pygame.image.load("sprites/base.png")
ground = pygame.transform.scale(ground, (384, 137))
ground_x = 0
ground2 = pygame.image.load("sprites/base.png")
ground2 = pygame.transform.scale(ground2, (384, 137))

# put bird image in a rect so your able to check collisions
bird = pygame.image.load("sprites/bluebird-midflap.png")
bird_rec = bird.get_rect(center=(100, 340))
bird_movement = 0

pipe = pygame.image.load("sprites/pipe-green.png")
pipe_up = pygame.image.load("sprites/pipe-green.png")
pipe_up = pygame.transform.flip(pipe_up, False, True)

# list of all pipes that come up
pipe_list = []

# creates an event that activates every 2300 time interval to spawn a pipe
SPAWN_P = pygame.USEREVENT
pygame.time.set_timer(SPAWN_P, 2300)

game_over = pygame.image.load("sprites/gameover.png")
# make game state true at the beginning
game_state = True
game_font = pygame.font.Font("04B_19__.TTF", 40)
# score initialized to zero
score = 0
# display the game with that screen
screen = pygame.display.set_mode((384, 683))

# loop runs until user exits
while True:
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # If user presses key
        if event.type == pygame.KEYDOWN:
            # if it was a space bar make the bird go up
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement += -6
            # If it was a space bar and not in a game restart game and re-initialize all the variables
            if event.key == pygame.K_SPACE and not game_state:
                game_state = True
                pipe_list.clear()
                bird_movement = 0
                bird_rec.center = (100, 340)
                pygame.time.set_timer(SPAWN_P, 2300)
                score = 0
        # call create pipe and return pipe on list if event happens
        if event.type == SPAWN_P:
            pipe_list.extend(create_pipe())

    # move ground to the left
    if ground_x == -384:
        ground_x = 0
    ground_x -= 1

    # Checks to make sure there is a pipe created so no error pops up
    # If so when the bird passes the center of the pipe increase the score
    if len(pipe_list) > 1:
        if pipe_list[len(pipe_list)-1].centerx == bird_rec.centerx:
            score += 1
    # bird moves down every second
    bird_movement += 0.2
    bird_rec.centery += bird_movement

    # call the function that returns a new pipe list that is moved to the left
    pipe_list = pipe_move(pipe_list)

    screen.blit(background, (0, 0))

    # If we are in the game
    if game_state:
        # Call check collision
        game_state = check_collision(pipe_list)
        # Draw the bird
        screen.blit(bird, bird_rec)
        # Draw the score
        write_score()
        # draw the pipes
        if len(pipe_list) > 1:
            if pipe_list[len(pipe_list)-1].top < 0:
                screen.blit(pipe_up, pipe_list[len(pipe_list)-1])
            else:
                screen.blit(pipe, pipe_list[len(pipe_list)-1])
            if pipe_list[len(pipe_list)-2].top < 0:
                screen.blit(pipe_up, pipe_list[len(pipe_list)-2])
            else:
                screen.blit(pipe, pipe_list[len(pipe_list)-2])
    # If we are not in a game call the write game over function
    else:
        write_game_over()

    # draw the the ground on the screen
    screen.blit(ground, (ground_x, 575))
    screen.blit(ground2, (ground_x + 384, 575))

    pygame.display.update()
    frame_rate.tick(120)

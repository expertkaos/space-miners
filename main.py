import pygame
import sys
import math
from spaceship import Spaceship
from pause_menu import PauseMenu

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Minners")

# Load background tile image
background_img = pygame.image.load("assets/space.jpg").convert()

# grab backround image width and height
bg_width = background_img.get_width()
bg_height = background_img.get_height()

bg_rect = background_img.get_rect()

# calculate how many tiles needed to fill screen
x_tiles = math.ceil(screen_width / bg_width) + 1
y_tiles = math.ceil(screen_height /bg_height) + 1

#Load spaceship images
SPACESHIP_IMG = pygame.image.load('assets/ship/spaceship.png').convert_alpha()
BOOSTED_SPACESHIP_IMG = pygame.image.load('assets/ship/boosted_spaceship.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60, 50))
BOOSTED_SPACESHIP_IMG = pygame.transform.scale(BOOSTED_SPACESHIP_IMG, (60, 50))

WHITE = (255, 255, 255)
FONT_SIZE = 36

# Create player sprite
spaceship = Spaceship([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], initial_angle=0, width=screen_width, height=screen_height)

all_sprites = pygame.sprite.Group()
all_sprites.add(spaceship)

running = True

# Create a PauseMenu instance
pause_menu = PauseMenu(width=screen_width, height=screen_height)

# Main game loop
running = True
while running:

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pause_menu.handle_event(event)
            if event.key == pygame.K_UP:
                spaceship.toggle()
            if event.key == pygame.K_ESCAPE:
                pause_menu.toggle()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                spaceship.toggle()
        else:
            pause_menu.handle_event(event)  # Handle button events

    
    if not pause_menu.is_paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.angle += spaceship.turn_speed
        if keys[pygame.K_RIGHT]:
            spaceship.angle -= spaceship.turn_speed
        if keys[pygame.K_UP]:
            spaceship.accelerate()
            
        spaceship.update()

        # Calculate the offset to center the player
        offset_x = screen_width // 2 - spaceship.rect.centerx
        offset_y = screen_height // 2 - spaceship.rect.centery

    # set background displacement
    x_displacement = spaceship.rect.centerx - (math.ceil(spaceship.rect.centerx / bg_width) * bg_width)
    y_displacement = spaceship.rect.centery - (math.ceil(spaceship.rect.centery / bg_height) * bg_height)
    
    # draw background tiles
    for x in range(-x_tiles, x_tiles):
        for y in range(-y_tiles, y_tiles):
            screen.blit(background_img, (x * bg_width +  x_displacement, y  * bg_height + y_displacement))

            #grid to display each background tile
            bg_rect.x = x * bg_width + x_displacement
            bg_rect.y= y * bg_height + y_displacement
            pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)
    
     # Draw spaceship
    screen.blit(spaceship.image, spaceship.rect.move(offset_x, offset_y))
    
    pause_menu.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

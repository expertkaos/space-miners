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
background_img = pygame.image.load("assets/space.jpg")

#Load spaceship images
SPACESHIP_IMG = pygame.image.load('assets/ship/spaceship.png').convert_alpha()
BOOSTED_SPACESHIP_IMG = pygame.image.load('assets/ship/boosted_spaceship.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60, 50))
BOOSTED_SPACESHIP_IMG = pygame.transform.scale(BOOSTED_SPACESHIP_IMG, (60, 50))

# Constants
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
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pause_menu.handle_event(event)
            if event.key == pygame.K_UP:
                spaceship.toggle()
                up_key_pressed = True
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

    # Draw background
    for x in range(-screen_width * 10, screen_width * 10, background_img.get_width()):
        for y in range(-screen_height * 10, screen_height * 10, background_img.get_height()):
            screen.blit(background_img, (x - offset_x, y - offset_y))

    # Draw spaceship
    screen.blit(spaceship.image, spaceship.rect.move(offset_x, offset_y))
    
    pause_menu.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

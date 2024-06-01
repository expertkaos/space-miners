import pygame
import sys

from spaceship import Spaceship
from pause_menu import PauseMenu
from background import Background
from planet import Planets

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Minners")

# Load assset images 

background_img = pygame.image.load("assets/space.jpg").convert()

SPACESHIP_IMG = pygame.image.load('assets/ship/spaceship.png').convert_alpha()
BOOSTED_SPACESHIP_IMG = pygame.image.load('assets/ship/boosted_spaceship.png').convert_alpha()

PLANETS_IMG = pygame.image.load('assets/planets.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60, 50))
BOOSTED_SPACESHIP_IMG = pygame.transform.scale(BOOSTED_SPACESHIP_IMG, (60, 50))

# Create class instance
spaceship = Spaceship([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], screen_width, screen_height)
background = Background(background_img, screen_width, screen_height)
pause_menu = PauseMenu(screen_width, screen_height)
planets = Planets(PLANETS_IMG)

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
        planets.update(spaceship_centerx=spaceship.rect.centerx, spaceship_centery=spaceship.rect.centery)
        background.update(spaceship_centerx=spaceship.rect.centerx, spaceship_centery=spaceship.rect.centery)

    background.draw(screen)
    planets.draw(screen)
    spaceship.draw(screen)

    pause_menu.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

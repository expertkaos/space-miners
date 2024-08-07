import pygame
import sys

from spaceship import Spaceship
from pause_menu import PauseMenu
from background import Background
from planet import Planets
from camera import Camera

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Minners")

# Load assset images 

background_img = pygame.image.load("assets/space.png").convert()

SPACESHIP_IMG = pygame.image.load('assets/ship/spaceship.png').convert_alpha()
BOOST_IMG = pygame.image.load('assets/ship/boost.png').convert_alpha()

PLANETS_IMG = pygame.image.load('assets/planets.png').convert_alpha()
EFFECT_IMG = pygame.image.load('assets/planets_fogs.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (50, 50))

# Create class instance
camera = Camera(screen)
background = Background(background_img, screen_width, screen_height, camera)
pause_menu = PauseMenu(screen_width, screen_height)
planets = Planets(PLANETS_IMG, EFFECT_IMG, camera)
spaceship = Spaceship(SPACESHIP_IMG, BOOST_IMG, screen_width, screen_height, camera, planets.planets_dict)

# Main game loop
running = True
while running:
    screen.fill((0,0,0))
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
            spaceship.rotate(-spaceship.turn_speed)
        if keys[pygame.K_RIGHT]:
            spaceship.rotate(+spaceship.turn_speed)
        if keys[pygame.K_UP]:
            spaceship.accelerate()
        
        grav = planets.get_gravity(spaceship.x, spaceship.y)
        spaceship.apply_gravity(grav[0], grav[1])

        spaceship.update()
        camera.update()

    background.draw()
    planets.draw()
    spaceship.draw()

    pause_menu.draw(screen)
    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
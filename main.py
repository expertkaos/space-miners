import pygame
import sys
import math
import os

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Minners")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load background tile image
background_img = pygame.image.load("space.jpg")

#Load spaceship images
SPACESHIP_IMG = pygame.image.load('ship/spaceship.png').convert_alpha()
BOOSTED_SPACESHIP_IMG = pygame.image.load('ship/boosted_spaceship.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60.6, 50))
BOOSTED_SPACESHIP_IMG = pygame.transform.scale(BOOSTED_SPACESHIP_IMG, (60.6, 50))

# Define spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, images, initial_angle=0):
        super().__init__()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.friction = 0.002
        self.turn_speed = 3

        self.images = images
        
        self.image_index_up_pressed = 1 # Image index when the up key is pressed
        self.image_index_up_released = 0 # Image index when the up key is released
        self.image = self.images[self.image_index_up_released] # Initially, set the image to the one displayed when the up key is released
        self.rect = self.image.get_rect()
        self.angle = initial_angle

    def rotate(self, angle_change):
        self.angle += angle_change
        self.image = pygame.transform.rotate([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def accelerate(self):
        rad_angle = math.radians(self.angle)
        self.velocity_y += self.acceleration * math.cos(rad_angle)
        self.velocity_x += self.acceleration * math.sin(rad_angle)

    def update(self):
        # Update the image based on whether the up key is pressed or released
        self.image = pygame.transform.rotate(self.images[self.image_index()], self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.velocity_x *= (1 - self.friction)  # Apply friction
        self.velocity_y *= (1 - self.friction)  # Apply friction
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def image_index(self):
        # Determine the current image index based on whether the up key is pressed
        if up_key_pressed:
            return self.image_index_up_pressed
        else:
            return self.image_index_up_released

# Create player sprite
spaceship = Spaceship([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], initial_angle=0)

all_sprites = pygame.sprite.Group()
all_sprites.add(spaceship)

running = True
up_key_pressed = False

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up_key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_key_pressed = False

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

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
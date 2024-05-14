import pygame
import math

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, images, initial_angle=0, width=800, height=600):
        super().__init__()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.friction = 0.002
        self.turn_speed = 3

        self.images = images

        self.up_key_pressed = False
        self.image_index_up_pressed = 1 # Image index when the up key is pressed
        self.image_index_up_released = 0 # Image index when the up key is released
        self.image = self.images[self.image_index_up_released] # Initially, set the image to the one displayed when the up key is released
        self.rect = self.image.get_rect()
        self.angle = initial_angle

        self.width = width
        self.height = height

    def rotate(self, angle_change):
        self.angle += angle_change
        self.image = pygame.transform.rotate(self.images[self.image_index()], self.angle)
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

        # an experiment to Ensure the spaceship stays within the screen bounds
        # self.rect.x %= self.width
        # self.rect.y %= self.height

    def image_index(self):
        
        if self.up_key_pressed:
            return self.image_index_up_pressed
        else:
            return self.image_index_up_released
        
    def toggle(self):
        self.up_key_pressed = not self.up_key_pressed
        
    

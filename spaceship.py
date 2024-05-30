import pygame
import math

from audio_manager import AudioManager

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, images, screen_width, screen_height):
        super().__init__()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.friction = 0.002
        self.turn_speed = 3

        self.audio_manager = AudioManager()  

        self.images = images

        self.up_key_pressed = False
        self.image_index_up_pressed = 1 # Image index when the up key is pressed
        self.image_index_up_released = 0 # Image index when the up key is released
        self.image = self.images[self.image_index_up_released] # Initially, set the image to the one displayed when the up key is released
        self.rect = self.image.get_rect()
        self.initial_angle = 0
        self.angle = self.initial_angle

        self.width = screen_width
        self.height = screen_height

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

        # Calculate the offset to center the player
        self.offset_x = self.width // 2 - self.rect.centerx
        self.offset_y = self.height // 2 - self.rect.centery

    def image_index(self):
        if self.up_key_pressed:
            return self.image_index_up_pressed
        else:
            return self.image_index_up_released
        
    def toggle(self):
        self.up_key_pressed = not self.up_key_pressed
        if self.up_key_pressed:
            self.audio_manager.play_boost_sound()
        else:
            self.audio_manager.stop_boost_sound()

    def draw(self, screen):
        screen.blit(self.image, self.rect.move(self.offset_x, self.offset_y))
        
    

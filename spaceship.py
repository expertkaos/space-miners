import pygame
import math
from audio_manager import AudioManager

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spaceship_image, trail_image, screen_width, screen_height):
        super().__init__()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.15
        self.friction = 0
        self.turn_speed = 3

        self.audio_manager = AudioManager()

        self.spaceship_image = spaceship_image
        self.trail_image = trail_image

        self.up_key_pressed = False
        self.image = self.spaceship_image
        self.rect = self.image.get_rect()

        # Set the ship location
        self.x = 0
        self.y = 0

        self.initial_angle = 0
        self.angle = self.initial_angle

        self.width = screen_width
        self.height = screen_height

        self.trails = []
        self.frame_counter = 0

    def rotate(self, angle_change):
        self.angle -= angle_change 
        self.image = pygame.transform.rotate(self.spaceship_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self):
        rad_angle = math.radians(self.angle)
        self.velocity_y += self.acceleration * math.cos(rad_angle)
        self.velocity_x += self.acceleration * math.sin(rad_angle)

    def apply_gravity (self, x, y):
        self.velocity_x += x
        self.velocity_y += y

    def update(self):
        self.frame_counter += 1
        if self.up_key_pressed and self.frame_counter % 4 == 0:  # Spawn trail every 4 frames
            self.spawn_trail()

        # Update trails
        self.trails = [trail for trail in self.trails if trail['alpha'] > 5 and  trail['size'] > 5]
        for trail in self.trails:
            trail['size'] -= 0.4  
            trail['image'] = pygame.transform.scale(self.trail_image, (int(trail['size']), int(trail['size'])))
            trail['alpha'] -= 5  # Decrease the alpha to fade out the trail
            trail['image'].set_alpha(trail['alpha'])
            trail['rotated_image'] = pygame.transform.rotate(trail['image'], trail['angle'])

        self.velocity_x *= (1 - self.friction)
        self.velocity_y *= (1 - self.friction)
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.image = pygame.transform.rotate(self.spaceship_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.offset_x = self.width // 2 - self.rect.centerx 
        self.offset_y = self.height // 2 - self.rect.centery 

    def spawn_trail(self):
        trail_size = 25  # Set the trail size to 25 pixels
        trail_image = pygame.transform.scale(self.trail_image, (trail_size, trail_size))
        trail_image.set_alpha(255)  # Set the initial alpha value

        # Calculate trail position based on the spaceship's angle
        trail_angle = self.angle
        rad_angle = math.radians(self.angle)
        trail_velocity_x = math.sin(rad_angle) * 5
        trail_velocity_y = math.cos(rad_angle) * 5

        # Define the radius of the circle around which the trail will spawn
        trail_radius = 35 

        # Calculate the offset from the center of the screen
        offset_x = trail_radius * math.sin(rad_angle)
        offset_y = trail_radius * - math.cos(rad_angle)

        # Calculate the trail's position around the circle
        trail_x = self.width // 2 + offset_x
        trail_y = self.height // 2 - offset_y  # Subtract to invert the y-axis

        self.trails.append({
            'image': trail_image,
            'rotated_image': pygame.transform.rotate(trail_image, trail_angle),
            'x': trail_x,
            'y': trail_y,
            'alpha': 255,  # Initial alpha value
            'size': trail_size,
            'vx': trail_velocity_x,
            'vy': trail_velocity_y,
            'angle': trail_angle 
        })

    def toggle(self):
        self.up_key_pressed = not self.up_key_pressed
        if self.up_key_pressed:
            self.audio_manager.play_boost_sound()
        else:
            self.audio_manager.stop_boost_sound()

    def draw(self, screen):
        for trail in self.trails:
            trail['x'] = trail['x'] + trail['vx'] 
            trail['y'] = trail['y'] + trail['vy']
            trail_rect = trail['rotated_image'].get_rect(center=(trail['x'], trail['y']))
            screen.blit(trail['rotated_image'], trail_rect)
        screen.blit(self.image, self.rect.move(self.offset_x, self.offset_y))

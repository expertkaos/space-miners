import pygame
import math
from audio_manager import AudioManager

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spaceship_image, trail_image, screen_width, screen_height, camera, planets_dict):
        super().__init__()
        
        self.camera = camera

        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.25
        self.friction = 0
        self.turn_speed = 3
        self.max_speed = 20
        self.speed = 0

        self.audio_manager = AudioManager()

        self.spaceship_image = spaceship_image
        self.trail_image = trail_image

        self.up_key_pressed = False
        self.image = self.spaceship_image
        self.rect = self.image.get_rect()

        # Set the ship beginning location
        self.x = 0
        self.y = 0

        self.initial_angle = 0
        self.angle = self.initial_angle

        self.width = screen_width
        self.height = screen_height

        self.trails = []
        self.frame_counter = 0

        self.planets_dict = planets_dict

    def rotate(self, angle_change):
        self.angle -= angle_change 
        self.image = pygame.transform.rotate(self.spaceship_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self):
        # initial speed
        rad_angle = math.radians(self.angle)
        self.velocity_y += self.acceleration * math.cos(rad_angle)
        self.velocity_x += self.acceleration * math.sin(rad_angle)

        # Limit the speed
        self.speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if self.speed > self.max_speed:
            scale = self.max_speed / self.speed
            self.velocity_x *= scale
            self.velocity_y *= scale

    def apply_gravity(self, x, y):
        self.velocity_x += x
        self.velocity_y += y

    def check_collision(self):
        '''Check distance to each planet and bounce if too close'''
         
        for planet_key, planet_data in self.planets_dict.items():
            planet_center_x = planet_data['x'] + planet_data['width'] // 2
            planet_center_y = planet_data['y'] + planet_data['height'] // 2
            planet_radius = max(planet_data['width'], planet_data['height']) // 2
            y_distance = self.y - planet_center_y
            x_distance = self.x - planet_center_x
            distance_to_planet = math.sqrt((x_distance)**2 + (y_distance)**2)
            
            if distance_to_planet < planet_radius + 25:
                self.camera.shake_camera(strength=5, duration=15)  
                self.camera.apply_shake()  
                # Calculate the normal vector at the point of collision
                normal_x = x_distance / distance_to_planet
                normal_y = y_distance / distance_to_planet

                # Calculate the dot product of the velocity vector and the normal vector
                dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y

                # Calculate the reflection vector
                reflection_x = self.velocity_x - 2 * dot_product * normal_x
                reflection_y = self.velocity_y - 2 * dot_product * normal_y

                # Apply the reflection vector to the ship's velocity
                self.velocity_x = reflection_x 
                self.velocity_y = reflection_y 

    def update(self):
        self.frame_counter += 1
        if self.up_key_pressed and self.frame_counter % 2 == 0:  # Spawn trail every 2 frames
            self.spawn_trail()

        # Update trails
        self.trails = [trail for trail in self.trails if trail['alpha'] > 5 and trail['size'] > 5]
        for trail in self.trails:
            trail['size'] -= 0.8 
            trail['image'] = pygame.transform.scale(self.trail_image, (int(trail['size']), int(trail['size'])))
            trail['alpha'] -= 10  # Decrease the alpha to fade out the trail
            trail['image'].set_alpha(trail['alpha'])
            trail['rotated_image'] = pygame.transform.rotate(trail['image'], trail['angle'])

        self.velocity_x *= (1 - self.friction)
        self.velocity_y *= (1 - self.friction)
        self.x -= self.velocity_x
        self.y -= self.velocity_y

        # Check for collisions
        self.check_collision()

        self.image = pygame.transform.rotate(self.spaceship_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.camera.moveCamera(self.x, self.y)

    def spawn_trail(self):
        trail_size = 30  # Set the trail size to 25 pixels
        trail_image = pygame.transform.scale(self.trail_image, (trail_size, trail_size))
        trail_image.set_alpha(255)  # Set the initial alpha value

        # Calculate trail position based on the spaceship's angle
        trail_angle = self.angle
        rad_angle = math.radians(self.angle)
        trail_velocity_x = math.sin(rad_angle) * 5
        trail_velocity_y = math.cos(rad_angle) * 5

        # Define the radius of the circle around which the trail will spawn
        trail_radius = 40

        # Calculate the offset from the spaceship's position
        offset_x = trail_radius * math.sin(rad_angle)
        offset_y = trail_radius * -math.cos(rad_angle)

        # Calculate the trail's position around the spaceship
        trail_x = self.rect.x + offset_x
        trail_y = self.rect.y - offset_y  # Subtract to invert the y-axis

        self.trails.append({
            'image': trail_image,
            'rotated_image': pygame.transform.rotate(trail_image, trail_angle),
            'x': trail_x,
            'y': trail_y,
            'alpha': 255,  # Initial alpha value
            'size': trail_size,
            'angle': trail_angle 
        })

    def toggle(self):
        self.up_key_pressed = not self.up_key_pressed
        if self.up_key_pressed:
            self.audio_manager.play_boost_sound()
        else:
            self.audio_manager.stop_boost_sound()

    def draw(self):
        for trail in self.trails:
            self.camera.drawImage(trail['rotated_image'], trail['x'] + 25 - (trail['size'] // 2), trail['y'] + 25 - (trail['size'] // 2))
        
        self.camera.drawImage(self.image, self.rect.x , self.rect.y)

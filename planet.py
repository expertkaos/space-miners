import pygame
import random
import math

PLANET_WIDTH = 500
PLANET_HEIGHT = 500
GRAVITY_STRENGTH = 17857
MAX_GRAVITY_DISTANCE = 1000
DISTANCE_STRECH = 1

AMOUNT_PLANETS = 10

class Planets(pygame.sprite.Sprite):

    def __init__(self, planet_image, camera):
        super().__init__()
        self.camera = camera
        self.planet_image = planet_image
        self.planet_rect = self.planet_image.get_rect()
        self.planet_distance = 0

        self.total_planets = 7 #how many images are in the sprite sheet
        self.planet_image_width = self.planet_image.get_width()
        
        self.planets_dict = {}
        self.planet_img = []

        self.planets_in_reach = 0

        for i in range(AMOUNT_PLANETS): 

            self.each_planet_img = pygame.Rect(random.randint(0, self.total_planets - 1) * (self.planet_image_width // self.total_planets), 0, 500, 500)
            self.planet_img.append(self.planet_image.subsurface(self.each_planet_img))
            
            planet_key = f"planet_{i}"
            self.planets_dict[planet_key] = {
                'image': self.planet_img[-1],
                'x': random.randint(-5000, 5000),
                'y': random.randint(-5000, 5000),
                'width': PLANET_WIDTH,
                'hight': PLANET_HEIGHT
            }
            
    
    def get_gravity(self, spaceship_centerx, spaceship_centery):
        gravity_x = 0
        gravity_y = 0

        planets_in_reach = 0

        for planet_key, planet_data in  self.planets_dict.items():

            x_planet_centre = planet_data['x']+ (planet_data['width']//2)
            y_planet_centre = planet_data['y']+ (planet_data['hight']//2)

            x_distance = x_planet_centre - spaceship_centerx 
            y_distance = y_planet_centre - spaceship_centery 

            planet_distance = math.sqrt(x_distance**2 + y_distance**2)  
            planet_gravity = (GRAVITY_STRENGTH / (planet_distance/DISTANCE_STRECH)**2)


            if planet_distance <= (PLANET_WIDTH//2) or planet_distance >= MAX_GRAVITY_DISTANCE:
                gravity_x += 0
                gravity_y += 0
            else:
                gravity_x += x_distance / planet_distance * planet_gravity
                gravity_y += y_distance / planet_distance * planet_gravity

                planets_in_reach += 1

        if planets_in_reach != 0:
            gravity_y = gravity_y / planets_in_reach
            gravity_x = gravity_x / planets_in_reach

        return (-gravity_x, -gravity_y)

    def draw(self, spaceship_centerx, spaceship_centery):    
        for planet_key, planet_data in self.planets_dict.items():
            self.camera.drawImage(planet_data['image'], planet_data['x'], planet_data['y'])

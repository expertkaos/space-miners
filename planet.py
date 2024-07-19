import pygame
import random
import math

PLANET_WIDTH = 500
PLANET_HEIGHT = 500
GRAVITY_STRENGTH = 17857
MAX_GRAVITY_DISTANCE = 1000
DISTANCE_STRECH = 1

AMOUNT_PLANETS = 50

class Planets(pygame.sprite.Sprite):

    def __init__(self, planet_image, effect_image, camera):
        super().__init__()
        self.camera = camera
        self.planet_image = planet_image
        self.effect_image = effect_image
        self.planet_rect = self.planet_image.get_rect()
        self.planet_distance = 0

        self.total_planets = 8 #how many images are in the sprite sheet
        self.total_effects = 4
        self.planet_image_width = self.planet_image.get_width()
        self.effect_image_width = self.effect_image.get_width()
        self.individual_effect_width = self.effect_image_width // self.total_effects
        
        self.planets_dict = {}
        self.planet_img = []
        self.effect_img = []

        self.planets_in_reach = 0

        for i in range(AMOUNT_PLANETS): 
            self.planet_image_number = random.randint(0, self.total_planets - 1)

            self.each_planet_img = pygame.Rect(self.planet_image_number * (self.planet_image_width // self.total_planets), 0, 500, 500)
            self.planet_img.append(self.planet_image.subsurface(self.each_planet_img))
            
            planet_key = f"planet_{i}"
            self.planets_dict[planet_key] = {
                'image': self.planet_img[-1],
                'image_number': self.planet_image_number,
                'x': random.randint(-10000, 10000),
                'y': random.randint(-10000, 10000),
                'width': PLANET_WIDTH,
                'height': PLANET_HEIGHT,
                'x_distance': 0,
                'y_distance': 0,
                'effect': None 
            }

        # Extract effect images
        for i in range(self.total_effects):
            self.each_effect_img = pygame.Rect(i * self.individual_effect_width, 0, 2000 ,2000)
            self.effect_img.append(self.effect_image.subsurface(self.each_effect_img))

        # Assign effects to planets
        effect_assignments = [0, 1, 1, 2, 3, 3, 3, 3]
        for planet_key, planet_data in self.planets_dict.items():
            for i, effect_index in enumerate(effect_assignments):
                if planet_data['image_number'] == i:
                    self.planets_dict[planet_key]['effect'] = self.effect_img[effect_index]

    
    def get_gravity(self, spaceship_centerx, spaceship_centery):
        gravity_x = 0
        gravity_y = 0

        planets_in_reach = 0
        min_distance = float('inf')  # Initialize minimum distance to infinity
        closest_planet_key = None  # Initialize closest planet key

        for planet_key, planet_data in  self.planets_dict.items():

            x_planet_centre = planet_data['x']+ (planet_data['width']//2)
            y_planet_centre = planet_data['y']+ (planet_data['height']//2)

            x_distance = x_planet_centre - spaceship_centerx 
            y_distance = y_planet_centre - spaceship_centery 

            planet_data['x_distance'] = x_distance
            planet_data['y_distance'] = y_distance

            planet_distance = math.sqrt(x_distance**2 + y_distance**2)  
            planet_gravity = (GRAVITY_STRENGTH / (planet_distance/DISTANCE_STRECH)**2)

            if planet_distance <= (PLANET_WIDTH//2) or planet_distance >= MAX_GRAVITY_DISTANCE:
                gravity_x += 0
                gravity_y += 0
            else:
                gravity_x += x_distance / planet_distance * planet_gravity
                gravity_y += y_distance / planet_distance * planet_gravity

                planets_in_reach += 1

            # Update minimum distance if the current planet is closer
            if planet_distance < min_distance:
                min_distance = planet_distance
                closest_planet_key = planet_key
                

        if planets_in_reach != 0:
            gravity_y = gravity_y / planets_in_reach
            gravity_x = gravity_x / planets_in_reach

        return (-gravity_x, -gravity_y)

    def draw(self):
        for planet_key, planet_data in self.planets_dict.items():
            if planet_data['effect'] != None:
                # Draw the effect image behind the planet
                self.camera.drawOffsetImage(planet_data['effect'], (planet_data['x'] - 1000 + (planet_data['width'] // 2)), (planet_data['y'] - 1000 + (planet_data['height'] // 2)), 0.8)

            # Draw planet
            self.camera.drawImage(planet_data['image'], planet_data['x'], planet_data['y'])
            

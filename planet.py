import pygame
import random
import math


PLANET_WIDTH = 500
PLANET_HEIGHT = 500
GRAVITY_STRENGTH = 17857
DISTANCE_STRECH = 1


class Planets(pygame.sprite.Sprite):

    def __init__(self, planet_image):
        super().__init__()
        self.planet_image = planet_image
        self.planet_rect = self.planet_image.get_rect()
        self.planet_distance = 0

        self.total_planets = 7
        self.planet_image_width = self.planet_image.get_width()
        
        self.planets_list = [ ]
        self.planet_img = [ ]
        for i in range(3):
            self.each_planet_img = pygame.Rect(random.randint(0, self.total_planets - 1) * (self.planet_image_width // self.total_planets), 0, 500, 500)
           
            self.planet_img.append(self.planet_image.subsurface(self.each_planet_img))
            
            self.planets_list.append((random.randint(-1000, 1000),random.randint(-1000, 1000)))
            
    def get_gravity(self, spaceship_centerx, spaceship_centery):
        gravity_x = 0
        gravity_y = 0
        for planet in self.planets_list:
            x_distance = planet[0] + (PLANET_WIDTH//2) - spaceship_centerx 
            y_distance = planet[1] + (PLANET_HEIGHT//2) - spaceship_centery 

            planet_distance = math.sqrt(x_distance**2 + y_distance**2)  
            if planet == self.planets_list[1]:
                print(planet_distance)
            planet_gravity = (1 / (planet_distance/DISTANCE_STRECH)**2) * GRAVITY_STRENGTH

            if planet_distance <= (PLANET_WIDTH//2):
                gravity_x += 0
                gravity_y += 0
            else:
                gravity_x += x_distance / planet_distance * planet_gravity
                gravity_y += y_distance / planet_distance * planet_gravity

        gravity_y = gravity_y / len(self.planets_list)
        gravity_x = gravity_x / len(self.planets_list)

        return (gravity_x, gravity_y)
            
    
    def update(self, spaceship_centerx, spaceship_centery):

        # set displacement
        self.x_displacement_planet = spaceship_centerx
        self.y_displacement_planet = spaceship_centery
        
    
    def draw(self, screen):    
        for i in range(len(self.planets_list)):
            screen.blit(self.planet_img[i], (self.planets_list[i][0] + self.x_displacement_planet, self.planets_list[i][1] + self.y_displacement_planet))
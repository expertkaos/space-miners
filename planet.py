import pygame
import random

class Planets(pygame.sprite.Sprite):
    def __init__(self, planet_image):
        super().__init__()
        self.planet_image = planet_image
        self.planet_rect = self.planet_image.get_rect()

        self.total_planets = 7
        self.planet_image_width = self.planet_image.get_width()
        
        self.planets_list = [ ]
        self.planet_img = [ ]
        for i in range(50):
            self.each_plannet_img = pygame.Rect(random.randint(0, self.total_planets - 1) * (self.planet_image_width // self.total_planets), 0, 500, 500)
           
            self.planet_img.append(self.planet_image.subsurface(self.each_plannet_img))
            
            self.planets_list.append((random.randint(-10000, 10000),random.randint(-10000, 10000)))

    
    def update(self, spaceship_centerx, spaceship_centery):
        self.spaceship_centerx = spaceship_centerx
        self.spaceship_centery = spaceship_centery

        # set displacement
        self.x_displacement_planet = self.spaceship_centerx
        self.y_displacement_planet = self.spaceship_centery
    
    def draw(self, screen):    
        
        for i in range(len(self.planets_list)):
            screen.blit(self.planet_img[i], (self.planets_list[i][0] + self.x_displacement_planet, self.planets_list[i][1] + self.y_displacement_planet))
            
            pygame.draw.rect(screen, (255, 0, 0), self.planet_img[i].get_rect(topleft=(self.planets_list[i][0] + self.x_displacement_planet, self.planets_list[i][1] + self.y_displacement_planet)), 2)

            # Get the position and radius for the circle
            circle_center = self.planets_list[i][0] + self.x_displacement_planet + 250, self.planets_list[i][1] + self.y_displacement_planet + 250
            circle_radius = 250  # Assuming the sprite is 500x500 pixels

            # Draw a circular perimeter around the sprite
            pygame.draw.circle(screen, (255, 0, 0), circle_center, circle_radius, 2)
        
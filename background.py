from typing import Any
import pygame
import math

class Background(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):


        self.background_img = image
        self.screen_width = screen_width
        self.screen_height = screen_height

        # grab backround image width and height
        self.bg_width = self.background_img.get_width()
        self.bg_height = self.background_img.get_height()

        self.bg_rect = self.background_img.get_rect()

        # calculate how many tiles needed to fill screen
        self.x_tiles = math.ceil(self.screen_width / self.bg_width) + 1
        self.y_tiles = math.ceil(self.screen_height / self.bg_height) + 1

    def update(self, spaceship_centerx, spaceship_centery):
        self.spaceship_centerx = spaceship_centerx
        self.spaceship_centery = spaceship_centery

        self.paralex_x = self.spaceship_centerx // 2 
        self.paralex_y = self.spaceship_centery // 2

        # set background displacement
        self.x_displacement = self.paralex_x  - (math.ceil(self.paralex_x / self.bg_width) * self.bg_width)
        self.y_displacement = self.paralex_y - (math.ceil(self.paralex_y / self.bg_height) * self.bg_height)
    
    def draw(self, screen):
        # draw background tiles
        for x in range(-self.x_tiles, self.x_tiles):
            for y in range(-self.y_tiles, self.y_tiles):
                screen.blit(self.background_img, (x * self.bg_width +  self.x_displacement, y  * self.bg_height + self.y_displacement))
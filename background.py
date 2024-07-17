from typing import Any
import pygame
import math
from camera import Camera

class Background(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height, camera):
        self.camera = camera
        self.background_img = image


    def draw(self):
        self.camera.drawTiles(self.background_img, 2)
from typing import Any
import math
import pygame
import random

class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        self.x_tiles = 0
        self.y_tiles = 0

        self.camera_area = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        
        self.Camera_centre_x = self.camera_area.x  - (self.screen_width // 2)
        self.Camera_centre_y = self.camera_area.y  - (self.screen_height / 2)

        # Shake parameters
        self.shake_duration = 0
        self.shake_strength = 0

        # Target position for the camera
        self.target_x = 0
        self.target_y = 0

    def moveCamera(self, x, y):
        self.target_x = x - (self.screen_width / 2)
        self.target_y = y - (self.screen_height / 2)

    def update(self):
        # Apply shake effect
        self.apply_shake()

        # Set the camera position
        self.camera_area.x = self.target_x
        self.camera_area.y = self.target_y

    def drawImage(self, image, x, y, paralex=1):
        coords = self.getScreenCoords(x, y, paralex)
        self.screen.blit(image, coords)

    def drawOffsetImage(self, image, x, y, offset):
        """Offset value is a fraction. Value of 1 equals no offset."""
        image_x, image_y = self.getScreenCoords(x, y)
        imagewidth = image.get_width()
        imageheight = image.get_height()
        centreImageX = image_x + imagewidth / 2
        centreImageY = image_y + imageheight / 2
        centreScreenX = self.screen_width / 2
        centreScreenY = self.screen_height / 2
        distanceX = centreScreenX - centreImageX
        distanceY = centreScreenY - centreImageY
        offsetX = distanceX * offset
        offsetY = distanceY * offset
        
        newCentreX = centreScreenX - offsetX 
        newCentreY = centreScreenY - offsetY 

        newX = newCentreX - imagewidth / 2
        newY = newCentreY - imageheight / 2

        offsetCoords = (newX, newY)
        self.screen.blit(image, offsetCoords)

    def drawTiles(self, image, paralex=1):
        screen_x = self.camera_area.x // paralex
        screen_y = self.camera_area.y // paralex

        image_width = image.get_width()
        image_height = image.get_height()

        x1 = math.floor(screen_x / image_width)
        y1 = math.floor(screen_y / image_height)
        x2 = math.ceil((screen_x + self.camera_area.width) / image_width)
        y2 = math.ceil((screen_y + self.camera_area.height) / image_height)

        for x in range(x1, x2):
            for y in range(y1, y2):
                self.drawImage(image, x * image_width, y * image_height, paralex)

    def drawCircle(self, colour, pos, radius, paralex=1):
        coords = self.getScreenCoords(pos[0], pos[1], paralex)
        pygame.draw.circle(self.screen, colour, coords, radius, 1)

    def getScreenCoords(self, x, y, paralex=1):
        return (x - (self.camera_area.x / paralex), y - (self.camera_area.y / paralex))

    def shake_camera(self, strength, duration):
        """Shake the camera with a given strength and duration."""
        self.shake_strength = strength
        self.shake_duration = duration

    def apply_shake(self):
        """Apply the shake effect to the camera."""
        if self.shake_duration > 0:
            shake_x = random.randint(-self.shake_strength, self.shake_strength)
            shake_y = random.randint(-self.shake_strength, self.shake_strength)
            self.target_x += shake_x
            self.target_y += shake_y
            self.shake_duration -= 1

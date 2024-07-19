from typing import Any
import math
import pygame

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

        # Camera settings
        self.camera_swithinpeed = 3
        self.camera_limit = 150  # Maximum distance the camera can lag behind


    def moveCamera(self, x, y):
        centre_x = x
        centre_y = y

        self.camera_area.x = centre_x - (self.screen_width/2)
        self.camera_area.y = centre_y - (self.screen_height/2)

    def update_camera(self, player_x, player_y):
        # Calculate the center of the camera
        cam_centre_x = self.camera_area.x + self.screen_width // 2
        cam_centre_y = self.camera_area.y + self.screen_height // 2

        # Calculate the difference between the player and the camera center
        diff_x = player_x - cam_centre_x
        diff_y = player_y - cam_centre_y

        # Define a smoothing factor (0 < smoothing < 1)
        smoothing = 0.1

        # Update camera position based on player position
        if abs(diff_x) > self.camera_limit:
            self.camera_area.x += diff_x - (self.camera_limit if diff_x > 0 else -self.camera_limit)
        else:
            self.camera_area.x += diff_x * smoothing  # Smoothly move towards the player

        if abs(diff_y) > self.camera_limit:
            self.camera_area.y += diff_y - (self.camera_limit if diff_y > 0 else -self.camera_limit)
        else:
            self.camera_area.y += diff_y * smoothing  # Smoothly move towards


    def drawImage(self,image, x, y, paralex = 1):
        coords = self.getScreenCoords(x, y, paralex)
        self.screen.blit(image, coords)

    
    def drawOffsetImage(self,image, x, y, offset): 
        """Offset value is a fraction. Value of 1 equls no offset.
        """
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

        newX =  newCentreX - imagewidth / 2
        newY = newCentreY - imageheight / 2

        offsetCoords = (newX, newY)
        self.screen.blit(image, offsetCoords)

    def drawTiles(self, image, paralex = 1):
        screen_x = self.camera_area.x // paralex
        screen_y = self.camera_area.y // paralex

        image_width = image.get_width() 
        image_height = image.get_height()

        x1 = math.floor(screen_x / image_width)
        y1 = math.floor(screen_y / image_height)
        x2 = math.ceil((screen_x + self.camera_area.width) / image_width)
        y2 = math.ceil((screen_y + self.camera_area.height) / image_height)

        for x in range(x1,x2):
            for y in range(y1,y2):
                self.drawImage(image, x * image_width, y * image_height, paralex)
    
    def drawCircle(self, colour, pos, radius, paralex = 1):
        coords = self.getScreenCoords(pos[0], pos[1], paralex)
        pygame.draw.circle(self.screen, colour, coords, radius, 1)

    def getScreenCoords(self, x, y, paralex = 1):
        return (x - (self.camera_area.x / paralex), y - (self.camera_area.y / paralex))


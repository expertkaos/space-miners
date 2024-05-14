import pygame
import sys
import math
import os


# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Minners")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load background tile image
background_img = pygame.image.load("space.jpg")

#Load spaceship images
SPACESHIP_IMG = pygame.image.load('ship/spaceship.png').convert_alpha()
BOOSTED_SPACESHIP_IMG = pygame.image.load('ship/boosted_spaceship.png').convert_alpha()

# Resize images
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60.6, 50))
BOOSTED_SPACESHIP_IMG = pygame.transform.scale(BOOSTED_SPACESHIP_IMG, (60.6, 50))

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
TRANSPARENT_BLACK = (0, 0, 0, 128)  # RGBA color with transparency
FONT_SIZE = 36

# Create a basic button class
class Button:
    def __init__(self, text, position, callback):
        self.text = text
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text_surface = self.font.render(text, True, WHITE)
        self.rect = self.text_surface.get_rect(center=position)
        self.callback = callback
        

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Create a basic pause menu class
class PauseMenu:
    def __init__(self):
        self.is_paused = False
        self.selected_button = 0  # Index of the currently selected button

        # Specify the path to your .ttf font file
        self.font_path = "pixelfont.ttf"
        self.font_size = 32

        self.custom_font = pygame.font.Font(self.font_path, self.font_size)# Load the font

        self.paused_text = self.custom_font.render("Game Paused", True, WHITE)
        
        self.buttons = [
            Button("Resume", (WIDTH // 2, HEIGHT // 2 - 0), self.resume_game),
            Button("Menu", (WIDTH // 2, HEIGHT // 2 + 75), self.quit_game),
            Button("Quit", (WIDTH // 2, HEIGHT // 2 + 150), self.quit_game),
        ]

        self.surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

    def toggle(self):
        self.is_paused = not self.is_paused

    def resume_game(self):
        self.toggle()  # Resume the game
        print("Resuming game...")  # Replace with your game logic

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def draw(self, screen):
        if self.is_paused:
            pygame.draw.rect(self.surface, (0,0,0,180),  [0, 0, WIDTH, HEIGHT])
            screen.blit(self.surface, (0,0))
            # Draw the "Game Paused" text
            text_rect = self.paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(self.paused_text, text_rect)

            # Draw the buttons
            # for button in self.buttons:
            #     button.draw(screen)

            for i, button in enumerate(self.buttons):
                button.draw(screen)
                if i == self.selected_button:
                    # Calculate the position for the arrow (to the left of the button)
                    arrow_x = button.rect.left - 20  # Place it to the left of the button
                    arrow_y = button.rect.centery

                    # Draw an arrow pointing to the side of the selected button
                    pygame.draw.polygon(screen, WHITE, [(arrow_x, arrow_y), (arrow_x - 20, arrow_y - 10), (arrow_x - 20, arrow_y + 10)])
            

    def handle_event(self, event):
        if self.is_paused:
            for button in self.buttons:
                button.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN: self.buttons[self.selected_button].callback()

# Define spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, images, initial_angle=0):
        super().__init__()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.friction = 0.002
        self.turn_speed = 3

        self.images = images
        
        self.image_index_up_pressed = 1 # Image index when the up key is pressed
        self.image_index_up_released = 0 # Image index when the up key is released
        self.image = self.images[self.image_index_up_released] # Initially, set the image to the one displayed when the up key is released
        self.rect = self.image.get_rect()
        self.angle = initial_angle

    def rotate(self, angle_change):
        self.angle += angle_change
        self.image = pygame.transform.rotate([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def accelerate(self):
        rad_angle = math.radians(self.angle)
        self.velocity_y += self.acceleration * math.cos(rad_angle)
        self.velocity_x += self.acceleration * math.sin(rad_angle)

    def update(self):
        # Update the image based on whether the up key is pressed or released
        self.image = pygame.transform.rotate(self.images[self.image_index()], self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.velocity_x *= (1 - self.friction)  # Apply friction
        self.velocity_y *= (1 - self.friction)  # Apply friction
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def image_index(self):
        # Determine the current image index based on whether the up key is pressed
        if up_key_pressed:
            return self.image_index_up_pressed
        else:
            return self.image_index_up_released

# Create player sprite
spaceship = Spaceship([SPACESHIP_IMG, BOOSTED_SPACESHIP_IMG], initial_angle=0)

all_sprites = pygame.sprite.Group()
all_sprites.add(spaceship)

running = True
up_key_pressed = False

# Create a PauseMenu instance
pause_menu = PauseMenu()

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pause_menu.handle_event(event)
            if event.key == pygame.K_UP:
                up_key_pressed = True
            if event.key == pygame.K_ESCAPE:
                pause_menu.toggle()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_key_pressed = False
        else:
            pause_menu.handle_event(event)  # Handle button events

    
    if not pause_menu.is_paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.angle += spaceship.turn_speed
        if keys[pygame.K_RIGHT]:
            spaceship.angle -= spaceship.turn_speed
        if keys[pygame.K_UP]:
            spaceship.accelerate()
            
        spaceship.update()

        # Calculate the offset to center the player
        offset_x = screen_width // 2 - spaceship.rect.centerx
        offset_y = screen_height // 2 - spaceship.rect.centery

    # Draw background
    for x in range(-screen_width * 10, screen_width * 10, background_img.get_width()):
        for y in range(-screen_height * 10, screen_height * 10, background_img.get_height()):
            screen.blit(background_img, (x - offset_x, y - offset_y))

    # Draw spaceship
    screen.blit(spaceship.image, spaceship.rect.move(offset_x, offset_y))
    
    pause_menu.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
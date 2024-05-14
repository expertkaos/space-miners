import pygame
import sys

class Button:
    def __init__(self, text, position, callback, width=800, height=600, font_size=36, white=(255, 255, 255)):
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, white)
        self.rect = self.text_surface.get_rect(center=position)
        self.callback = callback
        

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class PauseMenu:
    def __init__(self, width, height, font_size=36, white=(255, 255, 255)):
        self.is_paused = False
        self.selected_button = 0  # Index of the currently selected button

        self.font_path = "assets/pixelfont.ttf"
        self.font_size = font_size

        self.width, self.height = width, height

        self.custom_font = pygame.font.Font(self.font_path, self.font_size)# Load the font

        self.paused_text = self.custom_font.render("Game Paused", True, white)
        
        self.buttons = [
            Button("Resume", (width // 2, height // 2 - 0), self.resume_game, self.width, self.height),
            Button("Menu", (width // 2, height // 2 + 75), self.quit_game, self.width, self.height),
            Button("Quit", (width // 2, height // 2 + 150), self.quit_game, self.width, self.height),
        ]

        self.surface = pygame.Surface((width,height), pygame.SRCALPHA)

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
            pygame.draw.rect(self.surface, (0,0,0,180),  [0, 0, self.width, self.height])
            screen.blit(self.surface, (0,0))
            text_rect = self.paused_text.get_rect(center=(self.width // 2, self.height // 4))
            screen.blit(self.paused_text, text_rect)

            for i, button in enumerate(self.buttons):
                button.draw(screen)
                if i == self.selected_button:
                    arrow_x = button.rect.left - 20
                    arrow_y = button.rect.centery
                    pygame.draw.polygon(screen, (255, 255, 255), [(arrow_x, arrow_y), (arrow_x - 20, arrow_y - 10), (arrow_x - 20, arrow_y + 10)])
            

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

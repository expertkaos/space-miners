import pygame

class AudioManager:
    def __init__(self):
        self.music_libary = 'assets/music/' #set file locations

        # load sound effects
        self.boost_sound = pygame.mixer.Sound(self.music_libary + 'sound_effects/' + 'rocketnoise.mp3')
    
    def play_boost_sound(self):
        self.boost_sound.play(-1, fade_ms=300)
    
    def stop_boost_sound(self):
        self.boost_sound.fadeout(200)

    

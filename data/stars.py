import pygame
import data.game_functions as gf

class Stars():

    def __init__(self,ai_settings,screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image_url = gf.resource_path('data\\images\\stars.png')
        self.image = pygame.image.load(self.image_url).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    
    def blitme(self):
        
        self.screen.blit(self.image , self.rect)

    
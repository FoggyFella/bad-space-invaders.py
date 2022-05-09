import pygame
from pygame.sprite import Sprite
import data.game_functions as gf

class Alien(Sprite):

    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image_url = gf.resource_path('data\\images\\alien_game.png')
        self.image = pygame.image.load(self.image_url).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        self.x += (self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
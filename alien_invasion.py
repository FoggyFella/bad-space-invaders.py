import data.game_functions as gf
import pygame
from pygame.sprite import Group
from data.settings import Settings
from data.ship import Ship
from data.alien import Alien
from data.game_stats import GameStats
from data.button import Button
from data.scoreboard import ScoreBoard
from data.stars import Stars

def run_game():
    #Game window settings
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    pygame.display.set_icon(pygame.image.load(ai_settings.icon_path))
    #Making Ship
    ship = Ship(ai_settings, screen)
    #Groups for aliens and bullets
    bullets = Group()
    aliens = Group()
    #Making Alien
    alien = Alien(ai_settings,screen)
    #Making aliens fleet
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #Stats
    stats = GameStats(ai_settings,gf)
    #Play button
    play_button = Button(ai_settings,screen,'Play')
    #Score Board
    sb = ScoreBoard(ai_settings,screen,stats)
    #Stars
    stars = Stars(ai_settings,screen)



    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,stars,ship,aliens,bullets,play_button)   
        
         

            
        
  
run_game()
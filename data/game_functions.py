
import sys
import pygame
import os
import json
import random

from data.bullet import Bullet
from data.alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
        if event.key == pygame.K_RIGHT:
                ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                fire_bullet(ai_settings,screen,ship,bullets)
        elif event.key == pygame.K_q:
                sys.exit
                

def fire_bullet(ai_settings,screen,ship,bullets):
        if len(bullets) < ai_settings.bullets_allowed:
                new_bullet = Bullet(ai_settings,screen,ship)
                bullets.add(new_bullet)
                #sounds = ["sound\\laserSmall_000.ogg","sound\\laserSmall_001.ogg","sound\\laserSmall_002.ogg","sound\\laserSmall_003.ogg","sound\\laserSmall_004.ogg"]
                #sound = random.choice(sounds)
                shooty_url = resource_path("data\\sound\\laserSmall_000.ogg")
                shooty = load_sound(shooty_url)
                shooty.play()


def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
        if stats.ships_left > 0:
                stats.ships_left -= 1
                sb.prep_ships()
                boomy_url = resource_path("data\\sound\\explosionCrunch_000.ogg")
                boomy = load_sound(boomy_url)
                boomy.play()

                aliens.empty()
                bullets.empty()

                create_fleet(ai_settings,screen,ship,aliens)
                ship.center_ship()

                sleep(1)
        else:
                stats.game_active = False
                pygame.mouse.set_visible(True)

def check_keyup_events(event,ship):
        if event.key == pygame.K_RIGHT:
                ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                ship.moving_left = False


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             with open(ai_settings.filename,'w') as f_obj:
                json.dump(stats.high_score,f_obj)

                sys.exit()
        
        elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ai_settings,screen,ship,bullets)
        
        elif event.type == pygame.KEYUP:
                check_keyup_events(event,ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
        music_url = resource_path("data\\sound\\music.wav")
        music = load_sound(music_url)

        
        if button_clicked and not stats.game_active:
                ai_settings.initialize_dynamic_settings()
                stats.reset_stats()
                stats.game_active = True

                clicky_url = resource_path("data\\sound\\confirmation_003.ogg")
                clicky = load_sound(clicky_url)
                clicky.play()

                if stats.music_active == False:
                        music.play(-1)
                        stats.music_active = True
                        
                        
                elif stats.music_active == True:
                        music.stop()
                        
                        
                sb.prep_score()
                sb.prep_high_score()
                sb.prep_level()
                sb.prep_ships()

                aliens.empty()
                bullets.empty()
                pygame.mouse.set_visible(False)

                create_fleet(ai_settings,screen,ship,aliens)
                ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,stars,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
            bullet.draw_bullet()
    
    stars.blitme()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    if not stats.game_active:
            play_button.draw_button()
            
            


    pygame.display.flip()  

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):       
        collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
        if collisions:
                for aliens in collisions.values():
                        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats,sb)

        if len(aliens) == 0:
                bullets.empty()
                ai_settings.increase_speed()
                stats.level += 1
                sb.prep_level()
                create_fleet(ai_settings,screen,ship,aliens)

def check_high_score(stats,sb):
        if stats.score > stats.high_score:
                stats.high_score = stats.score
                sb.prep_high_score()


def get_number_aliens_x(ai_settings,alien_width):
        available_space_x = ai_settings.screen_width - (2 * alien_width)
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):

        available_space_y = (ai_settings.screen_height-(3*alien_height)- ship_height)
        number_rows = int(available_space_y / (2*alien_height))
        return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
        alien = Alien(ai_settings,screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
        alien = Alien(ai_settings,screen)
        number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
        number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
        
        for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                        create_alien(ai_settings,screen,aliens,alien_number,row_number)


def check_fleet_edges(ai_settings,aliens):
        for alien in aliens.sprites():
                if alien.check_edges():
                        change_fleet_direction(ai_settings,aliens)
                        break

def change_fleet_direction(ai_settings,aliens):
        for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

                        shooty_url = resource_path("data\\sound\\minimize_005.ogg")
                        shooty = load_sound(shooty_url)
                        shooty.play()
                        break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
        check_fleet_edges(ai_settings,aliens)
        aliens.update()

        if pygame.sprite.spritecollideany(ship,aliens):
                ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def get_high_score(ai_settings, stats):
        with open(ai_settings.filename) as f_obj:
                number = json.load(f_obj)
        stats.high_score = number
        return stats.high_score


        

        




main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir)

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pygame.mixer.Sound(fullname)

    return sound

def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)    

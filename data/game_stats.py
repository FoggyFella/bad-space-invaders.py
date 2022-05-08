import data.game_functions as gf


class GameStats():

    def __init__(self,ai_settings,gf):
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score = gf.get_high_score(ai_settings, self)
        self.music_active = False
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit 
        self.score = 0
        self.level = 1
        
    

        

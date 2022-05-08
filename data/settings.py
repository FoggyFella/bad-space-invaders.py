class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (46,59,102)
        #Ship settings
        
        self.ship_limit = 3
        #Bullet settings
        
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 226,147,28
        self.bullets_allowed = 3
        #Alien fleet settings
        
        self.fleet_drop_speed = 10
        

        self.speed_up_scale = 1.05
        self.score_scale = 1.5

        self.filename = "data\\user_data\\high_score_save.json"
        

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 0.8
        self.bullet_speed_factor = 2
        
        self.alien_speed_factor = 0.20
        self.alien_points = 10

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        
        
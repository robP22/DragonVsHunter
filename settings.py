from time import sleep

class Settings:
    """Class for managing game settings.
        Refactor to separate entity settings."""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        # self.bg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.text_bg_color = (255, 255, 255)

        self.fireball_width = 50
        self.fireball_height = 50
        self.fireball_radius = self.fireball_width / 2
        self.fireball_color = (255, 5, 0)

        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        
        self.dragon_lives = 3
        self.DEFAULT_HP = 100.0
        self.start_level = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #Screen display control
        self.toggle_full = False
        self.toggle_size_width = 0
        self.toggle_size_height = 0

        self.fireball_speed = 4.0
        self.fireball_limit = 3
        # self.fireball_damage = 20
        # self.fireball_cooldown = True -> sleep(1.0), False -> sleep(0.1)

        # self.bullet_damage = .5
        self.bullet_speed = 1.5
        self.bullet_limit = 3

        self.dragon_speed = 4.75
        self.dragon_health = 100.0

        self.hunter_speed = .15
        self.hunter_points = 5
        self.hunter_damage = 10
        self.army_speed_boost = 1.25
        # 1 for right, -1 for left
        self.army_direction = 1
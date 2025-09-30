class GameStats:
    def __init__(self, dvh_game):
        self.settings = dvh_game.settings
        self.dragon_god_mode_enable = False
        self.game_is_running = False
        self.high_score = 0

        self.read_high_score()
        self.reset_all_settings()
    
    def reset_all_settings(self):
        self.reset_hunter_stats()
        self.reset_player_character_stats()
        self.reset_level()
        self.reset_lives()
        self.reset_score()

    def reset_player_character_stats(self):
        """Resets player character stats."""
        self.dragon_health = self.settings.DEFAULT_HP
        self.dragon_speed = self.settings.dragon_speed
        self.fireball_speed = self.settings.fireball_speed
        self.fireball_limit = self.settings.fireball_limit

    def reset_hunter_stats(self):
        """Resets enemy sprites back to default."""
        self.hunter_speed = self.settings.hunter_speed
        self.hunter_points = self.settings.hunter_points
        self.hunter_dmg = self.settings.hunter_damage

    def reset_health(self):
        """Reset health to current maximum if 'God Mode' is not enabled."""        
        self.dragon_health = self.settings.dragon_health

    def reset_level(self):
        """Resets the session level back to 1."""
        self.level = self.settings.start_level

    def reset_lives(self):
        """Reset dragon lives count and _modifier count."""
        self.dragons_left = self.settings.dragon_lives

    def reset_score(self):
        """Resets the player score to 0"""
        self.score = 0

    def read_high_score(self):
        """
        Reads the highest score from a saved text file.
        Compares it to the current highest score.
        """
        try:
            with open('save_files/high_score.txt') as f:
                content = f.read()
                if content:
                    try:
                        content = int(content)
                        if content > self.high_score:
                            self.high_score = content
                    except ValueError:
                        print("Some sort of value error.")
        except FileNotFoundError:
            print("No high score file found.")

    def save_high_score(self):
        """
        Saves the current high score to a txt file.
        Should only be used in an if else block.
        """
        try:
            with open('save_files/high_score.txt', 'w') as f:
                f.write(str(int(self.high_score)))
        except FileNotFoundError:
            print('something went wrong...')
                
                
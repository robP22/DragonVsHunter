class Mods:
    def __init__(self, dvh_game):
        self.settings = dvh_game.settings
        self.stats = dvh_game.stats

    def _dragon_god_mode(self):
        self.stats.dragon_god_mode_enable = True
        self.stats.dragon_health = 1000000
        self.stats.dragon_lives = 1000000
        print(f"God mode enabled")
        print(f"-> Hp: {self.stats.dragon_health}")
        print(f"-> Lives: {self.stats.dragon_lives}")

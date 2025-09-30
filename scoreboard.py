import pygame
from pygame.sprite import Group
from dragon import Dragon

class Scoreboard:
    def __init__(self, dvh_game):
        """Initialize core scoreboard attributes"""
        self.dvh_game = dvh_game
        self.settings = dvh_game.settings
        self.stats = dvh_game.stats
        self.screen = dvh_game.screen
        self.screen_rect = dvh_game.screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    def _reposition_score(self, dvh_game):
        """Assist in repositioning entities when screen size is toggled."""
        self.screen = dvh_game.screen
        self.screen_rect = dvh_game.screen.get_rect()

    def prep_images(self):
        """Consolidates multiple image prep methods"""
        self.prep_score()
        self.check_high_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_dragons()

    def prep_score(self):
        """Renders the score integer as image after converting to string."""
        scr = int(self.stats.score)
        s_str = "Score: {:,}".format(scr)
        self.score_image = self.font.render(s_str, True, self.text_color, self.settings.text_bg_color)

        #display score in top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 20

    def prep_high_score(self):
        """Renders the high score integer as image after converting to string."""
        hs = int(self.stats.high_score)
        hs_str = "High Score: {:,}".format(hs)
        self.hs_img = self.font.render(hs_str, True, self.text_color, self.settings.text_bg_color)

        self.hs_rect = self.hs_img.get_rect()
        self.hs_rect.left = self.screen_rect.left + 20
        self.hs_rect.top = self.screen_rect.top + 20

    def prep_level(self):
        """Renders the level integer as image after converting to string."""
        lvl_str = f"Lvl: {self.stats.level}"
        self.lvl_img = self.font.render(lvl_str, True, self.text_color, self.settings.text_bg_color)
        
        self.level_rect = self.lvl_img.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.screen_rect.right - 20

    def prep_dragons(self):
        """Adds images of the player character in a row to represent lives."""
        self.dragons = Group()
        for dragon_number in range(self.stats.dragons_left):
            dragon = Dragon(self.dvh_game)
            dragon.image = pygame.image.load('images/base_dragon.png')
            dragon.rect = dragon.image.get_rect()
            dragon.rect.x = (self.screen_rect.width / 2) - dragon.rect.width + (
                dragon_number * dragon.rect.width) - 20
            dragon.rect.y = 10
            self.dragons.add(dragon)

    def check_high_score(self):
        """Check for new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

    def show_score(self):
        """Draw text to screen"""
        self.prep_images()
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hs_img, self.hs_rect)
        self.screen.blit(self.lvl_img, self.level_rect)
        self.dragons.draw(self.screen)
                
import pygame
from pygame.sprite import Sprite

class Dragon(Sprite):
    """Class for managing the dragon"""
    def __init__(self, dvh_game):
        super().__init__()
        """Initialize the dragon and its starting position."""
        self.settings = dvh_game.settings
        self.stats = dvh_game.stats
        self.screen = dvh_game.screen
        self.screen_rect = dvh_game.screen.get_rect()
        """ 
        Need to reset every module screen and screen rect object
        when the screen size is changed, therefore adjusting the position
        of all objects.
        """

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        #load dragon image
        self.image = pygame.image.load('images/dragon_battle.png')
        self.rect = self.image.get_rect()
        
        #assign start position, right middle
        self.rect.midright = self.screen_rect.midright

        #Store float for dragons vertical position
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        #Movement flags
        self.moving_up = False
        self.moving_down = False

        self.prep_health()

    def _reset_dragon_pos(self, dvh_game):
        """Assist in repositioning player character when screen size changes."""
        self.screen = dvh_game.screen
        self.screen_rect = dvh_game.screen.get_rect()

        self.rect.y = self.screen_rect.height / 2 - (self.rect.height / 2)
        self.rect.x = self.screen_rect.width - (self.rect.width)

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """
        If the player is pressing a movement key, move the character
        by a set amount. Update the rect object and then update the healthbar
        position to match, minus a buffer of 10px to reduce visual clutter.
        """
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.dragon_speed #Smaller numbers -> top of screen
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.dragon_speed #Larger numbers -> bottom of screen

        self.rect.y = self.y
        self.hlth_rect.bottom = self.rect.y - 10

    def prep_health(self):
        """Display the current health above head of player character."""
        hlth = int(self.stats.dragon_health)
        hlth_str = "Hp: {:,}".format(hlth)
        self.hlth_img = self.font.render(hlth_str, True, self.text_color, self.settings.text_bg_color)

        self.hlth_rect = self.hlth_img.get_rect()
        self.hlth_rect.bottom = self.rect.y - 10
        self.hlth_rect.left = ((self.rect.width - self.hlth_rect.width) / 2) + self.rect.left

    def blitme(self):
        """Draw the dragon at its current location"""
        self.prep_health()
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.hlth_img, self.hlth_rect)

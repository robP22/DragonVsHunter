import pygame
from pygame.sprite import Sprite
from random import randint

class Hunter(Sprite):
    def __init__(self, dvh_game):
        """Class for managing hunter enemies."""
        super().__init__()
        self.settings = dvh_game.settings
        self._random_speed()
        self.screen = dvh_game.screen
        self.screen_rect = self.screen.get_rect()
        self.battle_mode = True
        # self.battle_mode = False

        #load hunter image
        if self.battle_mode:
            self.image = pygame.image.load('images/hunter_battle.png')
        else:
            self.image = pygame.image.load('images/hunter_base.png')

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.rect.centerx = self.rect.height + self.rect.width / 2

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def _random_speed(self):
        """
        Unnecessary pseudo-random number modifier for speed.
        Theoretically always creates a number between 1 and 4.33.
        """
        rndm = (randint(3, 7) + randint(3, 19)) / 6
        self.speed = self.settings.hunter_speed * rndm

    def check_edges(self) -> bool:
        """Return True if hunter is at the edge of screen."""
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True
        return False
        
    def update(self):
        """
        Updates the x position by adding the current speed value.
        Updates the y position by adding a positive or negative integer.
        """
        self.rect.x += self.speed
        self.rect.y += (self.speed * self.settings.army_direction)

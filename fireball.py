import pygame
from pygame.sprite import Sprite

class Fireball(Sprite):
    def __init__(self, dvh_game):
        """Initialize the fireball and its starting position."""
        super().__init__()
        self.settings = dvh_game.settings
        self.screen = dvh_game.screen
        self.color = dvh_game.settings.fireball_color

        #Set the fireball position and then move it
        self.rect = pygame.Rect(0, 0, self.settings.fireball_width, 
                                self.settings.fireball_height)
        self.rect.midleft = dvh_game.dragon.rect.midleft

        #Store float for fireballs position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the position of fireball"""
        self.x -= self.settings.fireball_speed
        self.rect.x = self.x

    def draw_fireball(self):
        """Draw the dragon at its current location"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.settings.fireball_radius)
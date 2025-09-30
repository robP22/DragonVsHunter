import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, dvh_game):
        """Initialize the bullet and its starting position."""
        super().__init__()
        self.screen = dvh_game.screen
        self.settings = dvh_game.settings
        self.color = self.settings.bullet_color

        #Draw the bullet, then reposition
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midright = dvh_game.hunter.rect.midright

        #Store float for bullet position
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.bullet_speed

        #Update rect object position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet at its current location"""
        pygame.draw.rect(self.screen, self.color, self.rect)
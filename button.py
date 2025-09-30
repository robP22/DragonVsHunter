import pygame.font

class Button:

    def __init__(self, dvh_game, msg):
        """Initialize button attributes."""
        self.button_msg = msg
        self.screen = dvh_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set dimensions and properties of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Button message prep
        self._prep_msg(self.button_msg)

    def _reset_button_pos(self, dvh_game):
        """Assist in repositioning play button when screen size is toggled."""
        self.screen = dvh_game.screen
        self.screen_rect = dvh_game.screen.get_rect()
        self.rect.center = self.screen_rect.center
        self._prep_msg(self.button_msg)

    def _prep_msg(self, msg):
        """Turn msg into rendered image and center on button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
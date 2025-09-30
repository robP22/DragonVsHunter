import sys
from time import sleep

import pygame 

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from dragon import Dragon
from hunter import Hunter
from fireball import Fireball
from bullet import Bullet
from mods import Mods

class DragonVsHunter:
    """Class to manage game assets"""
    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()
        self.settings = Settings()
        self.main_loop = True

        #Set the default size to windowed
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        #Set the window title
        pygame.display.set_caption("Dragon Vs Hunter")

        #Create essential game objects
        self.clock = pygame.time.Clock()

        self.stats = GameStats(self)
        self.scrbrd = Scoreboard(self)
        self.dragon = Dragon(self)
        self.mods = Mods(self)

        self.fireballs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.hunters = pygame.sprite.Group()

        #Create the initial army
        self._create_army()

        #Create the play button
        self.play_button = Button(self, "Play Game")

    def _toggle_fullscreen(self):
        """Change the fullscreen setting."""
        if self.settings.toggle_full == False:
            self.settings.toggle_full = True 
        else:
            self.settings.toggle_full = False

    def _set_screen(self):
        """Set the screen to windowed or fullscreen.
        Need to refactor and create a screen manager class.
        The settings for the window stay locked to the default boundaries of
        1200x800px. this only happens after the play button is clicked so
        perhaps it has to do with some settings i am not reinitializing."""
        if self.settings.toggle_full == False:
            print(f"Windowed mode.")
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        else:
            print(f"Fullscreen Mode")
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Get window size
            self.settings.toggle_size_width = self.screen.get_rect().width
            self.settings.toggle_size_height = self.screen.get_rect().height
        
        self.scrbrd._reposition_score(self)
        self.play_button._reset_button_pos(self)
        self.dragon._reset_dragon_pos(self)

    def _check_events(self):
        """Interpret keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
            """Check if listed keys have been pressed."""
            if event.key == pygame.K_RALT:
                self._toggle_fullscreen()
                self._set_screen()
            elif event.key == pygame.K_UP:
                self.dragon.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.dragon.moving_down = True
            elif event.key == pygame.K_LALT:
                self.mods._dragon_god_mode()
            elif event.key == pygame.K_ESCAPE:
                self.main_loop = False
            elif event.key == pygame.K_SPACE:
                self._launch_fireball()
                #-- FIREBALL CONTROLS TO BE IMPLEMENTED LATER --
                # if event.key == pygame.K_w:
                #     self.fireballs.moving_up = True
                # elif event.key == pygame.K_s:
                #     self.fireballs.moving_down = True

    def _check_keyup_events(self, event):
            """Check if listed keys have been released."""
            if event.key == pygame.K_UP:
                self.dragon.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.dragon.moving_down = False
            # -- FIREBALL CONTROLS TO BE IMPLEMENTED LATER --
            # if event.key == pygame.K_w:
            #     self.fireballs.moving_up = False
            # elif event.key == pygame.K_s:
            #     self.fireballs.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks the button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_is_running:
            #fix dragon position reset
            self.stats.reset_all_settings()
            self._new_lvl()
            self.stats.game_is_running = True

            pygame.mouse.set_visible(False) #Hide cursor

    def _check_army_edges(self):
        """Change direction if any hunter touches an edge."""
        for hunter in self.hunters.sprites():
            if hunter.check_edges():
                self._change_army_direction()
                self._speed_boost()
                break
    
    def _check_army_dead(self):
        """
        Increases level counter.
        Resets sprites and player character position.
        Increases game difficulty.
        """
        if not self.hunters:
            self._lvl_diff_incr()
            self._new_lvl()
            self.stats.level += 1

    def _check_hunter_offscreen(self):
        """Detect when a hunter reaches the dragons home."""
        for hunter in self.hunters.copy():
            if pygame.sprite.spritecollideany(hunter, self.hunters):
                self._change_army_direction()
            if hunter.rect.right >= self.settings.screen_width:
                self.hunters.remove(hunter)
                self.take_damage()
                self._check_army_dead()

    def check_dragon_hp(self) -> int:
        """Returns 0 if the dragon is dead, 1 if the dragon is alive."""
        if self.stats.dragon_health <= 0:
            self._dragon_dead()
            return 0
        return 1

    def _check_dragon_hunter_collision(self):
        """Check for collisions between dragon and hunter group."""
        collision = pygame.sprite.spritecollideany(
                            self.dragon, self.hunters)
        if collision:
            self.hunters.remove(collision)
            self.stats.score += self.stats.hunter_points
            self.take_damage()
            self._check_army_dead()
    
    def _check_fireball_hunter_collisions(self):
        """Check for hunters hit by fireballs."""
        collisions = pygame.sprite.groupcollide(
                self.fireballs, self.hunters, False, True)
        if collisions:
            for hunters in collisions.values():
                self.stats.score += self.stats.hunter_points

        self.scrbrd.check_high_score()
        self._check_army_dead()

    def _create_hunter(self, hunter_number, column_number):
        """Create hunter enemy and add to sprite group."""
        hunter = Hunter(self)
        hunter_width, hunter_height = hunter.rect.size
        
        #spacing between hunters
        hunter.y = hunter_height + 2 * hunter_height * hunter_number + 10
        #y pos of each hunter
        hunter.rect.y = hunter.y + 45 #45 shifts each hunter downward
        """
        needs to just finish filling out the army or subtract the diff-
        erence between the screen size and the army size, then divide by 2
        to get the space above (and below) the army
        we know that calculating the army size is similar to the function
        _create_army(self)

        Will mean I have to refactor _create_hunter and _create_army so i can
        use the math in other functions
        """
        #x pos of each hunter
        hunter.rect.x = hunter_width + 2 * hunter_width * column_number - 2

        self.hunters.add(hunter)

    def _create_army(self):
        """Create an army of hunters."""
        hunter = Hunter(self)
        hunter_width, hunter_height = hunter.rect.size
        available_space_y = self.settings.screen_height - (2 * hunter_height)
        number_hunters_y = (available_space_y // (2 * hunter_height))

        #Determine the number of hunters that can fit on screen.
        dragon_width = self.dragon.rect.width
        available_space_x = (self.settings.screen_width - 
                            (8 * hunter_width) - dragon_width)
        number_columns = available_space_x // (3 * hunter_width)

        for column in range(number_columns):
            for hunter_number in range(number_hunters_y):
                self._create_hunter(hunter_number, column)

    def _change_army_direction(self):
        """Direction changer."""
        self.settings.army_direction *= -1

    def take_damage(self):
        """Simulate the dragon taking damage."""
        alive = self.check_dragon_hp()
        if alive:
            try:
                self.stats.dragon_health -= self.stats.hunter_dmg
            except ValueError:
                print('value is wrong somewhere.')
        self.check_dragon_hp()

    def _speed_boost(self):
        """Adding speed to the army."""
        for hunter in self.hunters.sprites():
            hunter.rect.x += self.settings.army_speed_boost

    def _launch_fireball(self):
        """Create new fireball and launch it."""
        if len(self.fireballs) < self.stats.fireball_limit:
            new_fireball = Fireball(self)
            self.fireballs.add(new_fireball)

    def _fire_bullet(self):
        """Create new bullet and fire it."""
        if len(self.bullets) < self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_fireball(self):
        """Update fireball position and remove old fireballs"""
        self.fireballs.update()

        for fireball in self.fireballs.copy():
            if fireball.rect.right <= 0:
                self.fireballs.remove(fireball)
    
    def _update_bullet(self):
        """Update fireball position and remove old fireballs."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

    def _update_hunters(self):
        """Update position of all hunters in the army."""
        self.hunters.update()
        self._check_army_edges()
        self._check_hunter_offscreen()
        self._check_dragon_hunter_collision()
        self._check_fireball_hunter_collisions()

    def _dragon_dead(self):
        """Simulate the dragon losing a life, Reset the level."""
        if self.stats.dragons_left >= 1:
            self.stats.dragons_left -= 1
            self.stats.fireball_limit += 1
            self.stats.level += 1
            self.stats.reset_health()
            self._new_lvl()
            sleep(0.5)
        else:
            self.stats.game_is_running = False
            pygame.mouse.set_visible(True)

    def _new_lvl(self):
        """Used to simulate a new level starting by resetting sprites."""
        if self.hunters:
            self.hunters.empty()
        self.fireballs.empty()
        self._create_army()
        self.dragon._reset_dragon_pos(self)

    def _lvl_diff_incr(self):
        """Increases the difficulty per level."""
        self.stats.hunter_speed += 0.15 * (self.stats.level * 0.08)
        self.stats.hunter_points += 5 * (self.stats.level * 0.08)
        self.stats.dragon_speed += 0.5 * (self.stats.level * 0.08)
        self.settings.dragon_health += 5 * (self.stats.level * 0.08)
        self.stats.fireball_speed += 0.5 * (self.stats.level * 0.08)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.dragon.blitme()
        self.hunters.draw(self.screen)
        self.scrbrd.show_score()
        
        if not self.stats.game_is_running:
            self.play_button.draw_button()
        else:
            for fireball in self.fireballs.sprites():
                fireball.draw_fireball()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

        pygame.display.flip()

    def run_game(self):
        """Main game loop"""
        while self.main_loop:
            self._check_events()

            if self.stats.game_is_running:
                self.dragon.update()
                self._update_hunters()
                self._update_fireball()
                self._update_bullet()

            self._update_screen()
            self.clock.tick(60)
            
        self.stats.read_high_score()
        self.stats.save_high_score()

if __name__ == '__main__':
    dvh = DragonVsHunter()
    dvh.run_game()
    sys.exit()

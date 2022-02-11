import pygame
import sys
from time import sleep

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resourses."""
        pygame.init()
        self.settings = Settings()
        self.screen = None

        self._set_screen_size()
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self.scoreboard = Scoreboard(self)

        self._create_fleet()

        # Set bg color.
        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                # Update the ship's behavior
                self.ship.update()
                # Update the bullets' behavior
                self._update_bullets()
                # Update the aliens behavior
                self._update_aliens()

            # Redrawn the screen during each pass through the loop
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Move the ship to the right.
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Move the ship to the left.
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            # Fire bullets from the ship.
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_aliens_bottom(self):
        """Check if any alien has reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.scoreboard.prep_level()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _create_alien(self, alien_position, row_position):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_position)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_position)
        self.aliens.add(alien)

    def _create_fleet(self):
        """Create the alien fleet."""
        # Make an alien and find how many fit in a row.
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens = available_space_x // (2 * alien_width)

        # Find how many rows fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_heigth) - ship_height
        number_rows = available_space_y // (2 * alien_heigth)

        # Create the fleet of aliens.
        for row_position in range(number_rows):
            for alien_position in range(number_aliens):
                self._create_alien(alien_position, row_position)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _set_screen_size(self):
        if self.settings.fullscreen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

    def _ship_hit(self):
        """Respond o the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of bullets that have disappeared."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for bullets that have hit aliens and then remove them.
        self._check_bullet_alien_collisions()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

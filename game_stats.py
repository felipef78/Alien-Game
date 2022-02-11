from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats:
    """Track statistics for the game."""

    def __init__(self, ai_game: 'AlienInvasion'):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.high_score = 0
        self.ships_left = None
        self.score = None
        self.level = None

        # Start Alien Invasion in inactive state.
        self.game_active = False

        self.reset_stats()

    def reset_stats(self):
        """Set the initial statistics."""
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level=1

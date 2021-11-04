from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats:
    """Track statistics for the game."""

    def __init__(self, ai_game: 'AlienInvasion'):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.ships_left = None

    # Start Alien Invasion in active state.
        self.game_active = True

        self.reset_stats()

    def reset_stats(self):
        """Set the initial statistics."""
        self.ships_left = self.settings.ships_limit

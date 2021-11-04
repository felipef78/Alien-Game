class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Alien settings.
        self.alien_speed = 1
        # fleet_direction of 1 is right; -1 is left
        self.fleet_direction = 1
        self.fleet_drop_speed = 5

        # Bullet settings.
        self.bullet_color = (60, 60, 60)
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_speed = 1.5
        self.bullets_allowed = 3

        # Screen settings.
        self.bg_color = (230, 230, 230)
        self.fullscreen_mode = False
        self.screen_height = 800
        self.screen_width = 1200

        # Ship settings.
        self.ship_speed = 1.5
        self.ships_limit = 3

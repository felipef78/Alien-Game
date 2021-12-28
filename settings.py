class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Alien settings.
        self.alien_speed = None
        self.fleet_drop_speed = 5
        self.fleet_direction = None

        # Bullet settings.
        self.bullet_color = (60, 60, 60)
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullets_allowed = 3
        self.bullet_speed = None

        # Screen settings.
        self.bg_color = (230, 230, 230)
        self.fullscreen_mode = False
        self.screen_height = 800
        self.screen_width = 1200

        # Ship settings.
        self.ship_speed = None
        self.ships_limit = 3

        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bullet_speed = 1.5
        self.ship_speed = 1.5

        # fleet_direction of 1 is right; -1 is left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale

class Settings:
    """Класс для хранения всех натсроек игры AlienInvasion"""


    def __init__(self):
        """Инициализирует настройки игры"""

        #параметры экрана
        self.full_mode = False
        self.window_width = 1280
        self.window_height = 720
        self.bg_color = (100, 100, 200)
        self.scale = 0.15

        self.spaceship_speed = 1.5
        self.ships_limit = 3

        self.bullet_speed = 2
        self.bullets_allowed = 100

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        self.alien_speed = 0.5
        self.fleet_drop_speed = 20
        self.fleet_direction = 1


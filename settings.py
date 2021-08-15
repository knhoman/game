class Settings:
    """Класс для хранения всех натсроек игры AlienInvasion"""


    def __init__(self):
        """Инициализирует настройки игры"""

        # инициализируем статические настройки
        # параметры экрана
        self.full_mode = False
        self.window_width = 1280
        self.window_height = 720
        self.bg_color = (100, 100, 200)
        self.scale = 0.15

        self.ships_limit = 3

        self.bullet_speed = 2
        self.bullets_allowed = 100

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        self.fleet_drop_speed = 20

        # темп ускорения игры
        self.speedup_scale = 1.2 # скорость увеличивается в полтора раза

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):

        # инициализируем настройки, изменяющиеся по ходу игры
        self.spaceship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        self.fleet_direction = 1

    def increase_speed(self):
        self.spaceship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
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

        self.spaceship_speed = 1.2

        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)


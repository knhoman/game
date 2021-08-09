class Settings:
    """Класс для хранения всех натсроек игры AlienInvasion"""


    def __init__(self):
        """Инициализирует настройки игры"""

        #параметры экрана
        self.window_width = 1280
        self.window_height = 720
        self.bg_color = (100, 100, 200)
        self.scale = 0.2
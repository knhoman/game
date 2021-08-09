import sys
import pygame

from settings import Settings
from spaceship import Spaceship

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption('AlienInvasion')

        self.spaceship = Spaceship(self)

    def run_game(self):
        """Запуск основного цикла игры"""

        while True:
            """Отслеживание событий клавиатуры и мыши"""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #При каждом проходе цикла перерисовывается экран
            self.screen.fill(self.settings.bg_color)
            self.spaceship.blitme()

            """Отображение последнего прорисоанного экрана"""
            pygame.display.flip()


if __name__ == '__main__':
    """Создание экземпляра класса и запуск игры"""

    ai = AlienInvasion()
    ai.run_game()
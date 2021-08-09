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
            #Отслеживание событий клавиатуры и мыши
            self._check_events()

            #обновление позиции корабля
            self.spaceship.update()

            #При каждом проходе цикла перерисовывается экран
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.spaceship.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.spaceship.moving_left = True
                if event.key == pygame.K_UP:
                    self.spaceship.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.spaceship.moving_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.spaceship.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.spaceship.moving_left = False
                if event.key == pygame.K_UP:
                    self.spaceship.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.spaceship.moving_down = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.spaceship.blitme()

        #отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    """Создание экземпляра класса и запуск игры"""

    ai = AlienInvasion()
    ai.run_game()
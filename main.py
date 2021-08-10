import sys
import pygame

from settings import Settings
from spaceship import Spaceship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""

        pygame.init()
        self.settings = Settings()

        if self.settings.full_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.window_width = self.screen.get_rect().width
            self.settings.window_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))

        pygame.display.set_caption('AlienInvasion')

        self.spaceship = Spaceship(self)

        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Запуск основного цикла игры"""

        while True:
            # Отслеживание событий клавиатуры и мыши
            self._check_events()

            # обновление позиции корабля
            self.spaceship.update()

            # обновление позиции снаряда, метод update() применяется ко всем элементам группы
            self.bullets.update()

            # удаление снарядов, вышежших за пределы экрана
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            # При каждом проходе цикла перерисовывается экран
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = True
        elif event.key == pygame.K_UP:
            self.spaceship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.spaceship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = False
        elif event.key == pygame.K_UP:
            self.spaceship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.spaceship.moving_down = False

    def _fire_bullet(self):
        # создание нового снаряда и включение его в группу bullets
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.spaceship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    """Создание экземпляра класса и запуск игры"""

    ai = AlienInvasion()
    ai.run_game()

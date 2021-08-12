import sys
import pygame

from settings import Settings
from spaceship import Spaceship
from bullet import Bullet
from alien import Alien


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

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Запуск основного цикла игры"""

        while True:
            # Отслеживание событий клавиатуры и мыши
            self._check_events()

            # обновление позиции корабля
            self.spaceship.update()

            # обновление позиции снаряда и удаление снарядов, вышедших за экран
            self._update_bullets()

            # движение пришельцев
            self._update_aliens()

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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # обновление позиции снаряда, метод update() применяется ко всем элементам группы
        self.bullets.update()

        # удаление снарядов, вышежших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # проверка попаданий в пришельцев
        # при обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _create_fleet(self):
        # создание флота
        alien = Alien(self)
        # определение ширины и высоты из размеров прямоугольника иконки пришельца
        alien_width, alien_height = alien.rect.size
        spaceship_height = self.spaceship.rect.height
        # определение числа пришельцев в ряду
        available_space_x = self.settings.window_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = self.settings.window_height - spaceship_height - (3 * alien_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            #создание первого ряда пришельцев
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_width * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # реагирует на достижение пришельцем края экрана
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.spaceship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    """Создание экземпляра класса и запуск игры"""

    ai = AlienInvasion()
    ai.run_game()

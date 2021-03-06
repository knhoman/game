import sys
import pygame

from settings import Settings
from spaceship import Spaceship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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

        # создание экземпляра для хранения статистики текущей игры
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.spaceship = Spaceship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Запуск основного цикла игры"""

        while True:
            # Отслеживание событий клавиатуры и мыши
            self._check_events()

            if self.stats.game_status:
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):

        # проверяет произошло ли нажатие кнопки Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_status:

            # задаем начальные параметры скорости игры
            self.settings.initialize_dynamic_settings()

            # сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_status = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            # очистка списков снарядов и пришельце
            self.bullets.empty()
            self.aliens.empty()

            # создание нового флота и помещение корабля в начальную позицию
            self._create_fleet()
            self.spaceship.center_ship()

            # скроем указать мыши во время игры
            pygame.mouse.set_visible(False)

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

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):

        # проверка попаданий в пришельцев
        # при обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()
            self._create_fleet()


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
            # создание первого ряда пришельцев
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

        # проверка коллизий корабля и группы пришельцев
        if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
            self._spaceship_hit()

        # проверка добрался ли хоть один пришелец до нижней границы экрана
        self._check_aliens_bottom()

    def _spaceship_hit(self):
        # уменьшение числа жизней при столкновении корабля с пришельцем
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # очистка списков снарядов и пришельцев
            self.aliens.empty()
            self.bullets.empty()
            self.scoreboard.prep_ships()

            # создание нового флота пришельцев и помещение корябля в начальную позицию
            self._create_fleet()
            self.spaceship.center_ship()

            # пауза
            pygame.time.wait(500)

        else:
            self.stats.game_status = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # проверяет добрались ли пришельцы до нижнего края экрана
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._spaceship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.spaceship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # вывод информации о счете
        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        # кнопка Play будет отображаться в том случае, если игра не активна
        if not self.stats.game_status:
            self.play_button.draw_button()

        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    """Создание экземпляра класса и запуск игры"""

    ai = AlienInvasion()
    ai.run_game()

import pygame.font
from pygame.sprite import Group
from spaceship import Spaceship

class Scoreboard:

    # класс для вывода игровой инфорации
    def __init__(self, ai_game):

        # инициализируем атрибуты подсчета очков
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # подготовка исходного изображения
        self.prep_score()

        # рекорд
        self.prep_high_score()

        # текущий уровень
        self.prep_level()

        # количество жизней
        self.prep_ships()

    def prep_score(self):

        # преобразуем текущий текст в изображение
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):

        # преобразуем текущий текст в изображение
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # вывод счета в верхней части экрана по центру
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):

        # преобразуем текст в изображение
        current_level_str = str(self.stats.level)
        self.current_level_image = self.font.render(current_level_str, True, self.text_color, self.settings.bg_color)

        # вывод текущего уровня в левом верхнем углу
        self.current_level_rect = self.current_level_image.get_rect()
        self.current_level_rect.right = self.screen_rect.right - 20
        self.current_level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):

        # выводит количество оставшихся жизней
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Spaceship(self.ai_game)
            ship.rect.x = 20 + ship_number * ship.rect.width
            ship.rect.y = 20
            self.ships.add(ship)

    def show_score(self):

        # выводим счет на эран
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.current_level_image, self.current_level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):

        # првоеряем больше ли текущий счет, чем предыдущий рекорд
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

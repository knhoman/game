import pygame

class Spaceship:
    """Класс для управления кораблем"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """Загружает изображение корабля и получает прямоугольник"""
        self.image = pygame.image.load('icons/spaceship.png')

        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(x*self.settings.scale), int(y*self.settings.scale)))

        self.rect = self.image.get_rect()

        self.center_ship()

        #флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        #обновляет позицию корабля с учетом флагов self.moving_
        #обновляются атрибуты self.x и self.y, а не self.rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.spaceship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.spaceship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.spaceship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.spaceship_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):
        """Рисует корабль в текущей позиции"""

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # помещение корабля в начальную позицию
        # каждый новый корабль появляется в центре низа экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # сохранение вещественной координаты центра корябля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
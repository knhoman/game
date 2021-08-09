import pygame

class Spaceship:
    """Класс для управления кораблем"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """Загружает изображение корабля и получает прямоугольник"""
        self.image = pygame.image.load('icons/spaceship.svg')

        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(x*self.settings.scale), int(y*self.settings.scale)))

        self.rect = self.image.get_rect()

        #каждый новый корабль появляется в центре низа экрана
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        #обновляет позицию корабля с учетом флага self.moving_
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_up:
            self.rect.y -= 1
        if self.moving_down:
            self.rect.y += 1


    def blitme(self):
        """Рисует корабль в текузей позиции"""

        self.screen.blit(self.image, self.rect)
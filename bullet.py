import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #класс для выстрела

    def __init__(self, ai_game):
        super().__init__()

        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.color = self.settings.bullet_color

        #создание прямоугольника в позиции (0, 0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.spaceship.rect.midtop

        #позиция снаряда хранится в везщественном формате
        self.y = float(self.rect.y)

    #перемещение снаряда вверх по экрану
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    #отрисовка прямоугольника
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
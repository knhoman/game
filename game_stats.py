class GameStats:

    # статистика для игры
    def __init__(self, ai_game):
        # инициализация статистики
        self.settings = ai_game.settings
        self.reset_stats()

        # игра запускается в неактивном состоянии
        self.game_status = False

        # рекорды
        self.high_score = 0

    def reset_stats(self):

        # инициализирует статистику, изменяющуюся в ходе игры
        self.ships_left = self.settings.ships_limit

        # подсчет очков
        self.score = 0

        # текущий уровень
        self.level = 1



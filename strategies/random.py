import random

class Random:
    name = 'Random'

    def get_move(self, game, all_moves):
        return random.choice(all_moves)
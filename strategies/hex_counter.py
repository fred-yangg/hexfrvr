import random

from utils import indices

class HexCounter:
    name = 'Hex Counter'

    def get_move(self, game, all_moves):
        def rank_move(move):
            lookahead = game.copy()
            lookahead.play_hand(*move)
            return sum(hexagon_value for hexagon_value in lookahead.board.values())

        ranked_moves = sorted(map(lambda move: (rank_move(move), move), all_moves))
        top_moves = list(filter(lambda ranked_move: ranked_move[0] == ranked_moves[0][0], ranked_moves))

        return random.choice(top_moves)[1]
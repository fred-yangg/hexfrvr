import random

from utils import tadd


class EmptinessMaximizationWithDotBias:
    name = 'Emptiness Maximization w/ Dot Bias'

    def get_move(self, game, all_moves):
        checks = [(1,0), (0,1), (1,1)]
        dot = ((0,0),(0,0),(0,0),(0,0))
        def rank_move(move):
            piece_num, position = move
            piece = game.hand[piece_num]

            if piece == dot:
                dot_bias = -100000
            else:
                dot_bias = 0

            lookahead = game.copy()
            lookahead.play_hand(*move)

            score = dot_bias
            for index, filled in lookahead.board.items():
                if not filled:
                    for check in checks:
                        coord = tadd(index, check)
                        score += coord in lookahead.board and not lookahead.board[coord]
            return score

        ranked_moves = sorted(map(lambda move: (rank_move(move), move), all_moves), reverse=True)
        top_moves = list(filter(lambda ranked_move: ranked_move[0] == ranked_moves[0][0], ranked_moves))

        return random.choice(top_moves)[1]

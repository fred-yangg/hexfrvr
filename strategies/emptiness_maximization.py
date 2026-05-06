import random

from utils import tadd


class EmptinessMaximization:
    name = 'Emptiness Maximization'

    def get_move(self, game, all_moves):
        checks = [(1,0), (0,1), (1,1)]
        def rank_move(move):
            lookahead = game.copy()
            lookahead.play_hand(*move)

            score = 0
            for index, filled in lookahead.board.items():
                if not filled:
                    for check in checks:
                        coord = tadd(index, check)
                        score += coord in lookahead.board and not lookahead.board[coord]
            return score

        ranked_moves = sorted(map(lambda move: (rank_move(move), move), all_moves), reverse=True)
        top_moves = list(filter(lambda ranked_move: ranked_move[0] == ranked_moves[0][0], ranked_moves))

        return random.choice(top_moves)[1]

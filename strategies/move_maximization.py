from collections import defaultdict

import random

from game import piece_bag, in_bounds_moves_by_piece
from utils import tadd, build_probabilities_by_piece

probabilities_by_piece = build_probabilities_by_piece(piece_bag)

class MoveMaximization:
    name = 'Move Maximization'

    def get_move(self, game, all_moves):
        def rank_move(move):
            carry_forward_hand = game.hand.copy()
            carry_forward_hand.remove(move[0])
            lookahead = game.copy()
            lookahead.play_hand(*move)

            playable_move_count_by_piece = defaultdict(int)
            for piece, positions in in_bounds_moves_by_piece.items():
                for position in positions:
                    if lookahead.check_move_collision(piece, position):
                        playable_move_count_by_piece[piece] += 1

            score = 0
            for piece, count in playable_move_count_by_piece.items():
                weighting = carry_forward_hand.count(piece) + probabilities_by_piece[piece]
                score += weighting * count

            return score

        ranked_moves = sorted(map(lambda move: (rank_move(move), move), all_moves), reverse=True)
        top_moves = list(filter(lambda ranked_move: ranked_move[0] == ranked_moves[0][0], ranked_moves))

        return random.choice(top_moves)[1]

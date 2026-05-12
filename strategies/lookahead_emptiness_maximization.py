import random
from pygments.lexers.sql import lookahead

from game import Game
from utils import tadd, indices


def to_hashable(game):
    sorted_hand = tuple(sorted(game.hand))

    board_int = 0
    curr = 1
    for position in enumerate(indices()):
        if game.board[position]:
            board_int += curr
        curr <<= 1
    return sorted_hand, board_int

class LookaheadEmptinessMaximization:
    name = 'Lookahead Emptiness Maximization'

    def __init__(self, lookahead_depth=1):
        self.lookahead_depth = lookahead_depth

    def get_move(self, game: Game, all_moves):
        ranked_moves = []

        def rank(board):
            checks = [(1,0), (0,1), (1,1)]
            score = 0
            for index, filled in board.items():
                if not filled:
                    for check in checks:
                        coord = tadd(index, check)
                        score += coord in board and not board[coord]
            return score

        def visit(game: Game, moves_so_far, ranks_so_far):

            # ran out of pieces or reached max lookahead depth, rank state with moves and return
            if not game.hand or len(moves_so_far) >= self.lookahead_depth:
                ranked_moves.append((ranks_so_far, moves_so_far[0]))
                return

            # not a repeat or terminal state, continue searching
            for move in game.all_playable_moves():
                lookahead = game.copy()
                lookahead.play_hand(*move, replacement=False)
                lookahead_rank = rank(lookahead.board)
                visit(
                    lookahead,
                    moves_so_far + (move,),
                    (lookahead_rank,) + ranks_so_far
                )

        visit(game, (), ())

        ranked_moves.sort(reverse=True)
        top_rank = ranked_moves[0][0]
        top_moves = []
        for rank, move in ranked_moves:
            if rank == top_rank:
                top_moves.append(move)
            else:
                break

        return random.choice(top_moves)

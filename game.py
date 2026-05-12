import random

from utils import indices, piece_hexes, build_line_checks_by_move, build_in_bounds_moves_by_piece

type Position = tuple[int, int]
type Piece = tuple[Position, ...]
type Move = tuple[Piece, Position]
piece_bag: list[Piece] = [
    # lines
    ((0,0), (1,0), (2,0), (3,0)), # /
    ((0,0), (1,0), (2,0), (3,0)), # /
    ((0,0), (1,1), (2,2), (3,3)), # \
    ((0,0), (1,1), (2,2), (3,3)), # \
    ((0,0), (0,1), (0,2), (0,3)), # -
    ((0,0), (0,1), (0,2), (0,3)), # -

    # rombus
    ((0,0), (0,1), (1,0), (1,1)), # S
    ((0,0), (0,1), (1,0), (1,1)), # S
    ((0,0), (0,1), (1,1), (1,2)), # Z
    ((0,0), (0,1), (1,1), (1,2)), # Z
    ((0,0), (1,0), (1,1), (2,1)), # O
    ((0,0), (1,0), (1,1), (2,1)), # O

    # cups
    ((0,0), (1,0), (2,1), (2,2)), # ( up tilt
    ((0,0), (0,1), (1,0), (2,1)), # ( down tilt
    ((0,0), (1,1), (2,0), (2,1)), # ) up tilt
    ((0,0), (0,1), (1,2), (2,2)), # ) down tilt
    ((0,0), (1,1), (1,2), (0,2)), # u
    ((0,0), (0,1), (1,0), (1,2)), # n

    # dot
    ((0,0),),
    ((0,0),),
    ((0,0),),
    ((0,0),),
    ((0,0),),
    ((0,0),),

    # P shapes
    ((0,0), (0,1), (1,1), (2,2)),   # P up tilt
    ((0,0), (1,0), (1,1), (2,0)),   # P down tilt
    ((0,0), (1,0), (2,0), (1,-1)),  # d up tilt
    ((0,0), (1,1), (2,2), (2,1)),   # d down tilt
    ((0,0), (0,1), (0,2), (1,2)),   # P face down
    ((0,0), (1,0), (1,1), (1,2)),   # P face up

    # L shapes
    ((0,0), (1,1), (2,2), (1,2)),   # L up tilt
    ((0,0), (1,0), (2,0), (2,1)),   # L down tilt
    ((0,0), (0,1), (1,1), (2,1)),   # 7 up tilt
    ((0,0), (1,0), (1,1), (2,2)),   # 7 down tilt
    ((0,0), (0,1), (0,2), (1,1)),   # L face down
    ((0,0), (1,0), (1,1), (1,-1)),  # L face up
]

piece_types: set[Piece] = set(piece_bag)

line_checks_by_move: dict[Move, list[set[Position]]] = build_line_checks_by_move(piece_types)

in_bounds_moves_by_piece: dict[Piece, set[Position]] = build_in_bounds_moves_by_piece(piece_types)

class Game:
    def __init__(self):
        self.hand_size = 3
        self.board = {index: False for index in indices()}
        self.hand = random.choices(piece_bag, k=self.hand_size)
        self.dead = False
        self.move_count = 0

    def reset(self):
        self.board = {index: False for index in indices()}
        self.hand = random.choices(piece_bag, k=self.hand_size)
        self.dead = False
        self.move_count = 0

    def copy(self):
        game = Game()
        game.board = self.board.copy()
        game.hand = self.hand.copy()
        game.dead = self.dead
        game.move_count = self.move_count
        return game

    def play_strategy(self, strategy):
        all_moves = self.all_playable_moves()

        if not all_moves:
            self.dead = True
            return None

        if len(all_moves) == 1:
            move = all_moves[0]
        else:
            move = strategy.get_move(self, all_moves)

        move_hexes = piece_hexes(*move)
        self.play_hand(*move)
        return move_hexes

    def clear(self, hexes):
        for hexagon in hexes:
            self.board[hexagon] = False

    def fill(self, hexes):
        for hexagon in hexes:
            self.board[hexagon] = True

    def check_move_collision(self, piece, position):
        for hexagon in piece_hexes(piece, position):
            if self.board[hexagon]:
                return False

        return True

    def all_playable_moves(self) -> list[Move]:
        return [
            (piece, position)
            for piece in set(self.hand)
            for position in in_bounds_moves_by_piece[piece]
            if self.check_move_collision(piece, position)
        ]

    def place_piece(self, piece, position):
        self.fill(piece_hexes(piece, position))

    def play_hand(self, piece, position, replacement=True):
        self.place_piece(piece, position)

        if replacement:
            piece_num = self.hand.index(piece)
            self.hand[piece_num] = random.choice(piece_bag)
        else:
            self.hand.remove(piece)

        self.perform_line_clears(piece, position)
        self.move_count += 1

    def perform_line_clears(self, piece, position):
        checks = line_checks_by_move[(piece, position)]
        to_clear = set()

        for line in checks:
            full = True
            for hexagon in line:
                if not self.board[hexagon]:
                    full = False
                    break

            if full:
                to_clear |= line

        self.clear(to_clear)
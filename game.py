import random

from utils import indices, piece_hexes, build_piece_checks

piece_bag = [
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
    ((0,0), (0,0), (0,0), (0,0)),
    ((0,0), (0,0), (0,0), (0,0)),
    ((0,0), (0,0), (0,0), (0,0)),
    ((0,0), (0,0), (0,0), (0,0)),
    ((0,0), (0,0), (0,0), (0,0)),
    ((0,0), (0,0), (0,0), (0,0)),
]

piece_types = set(piece_bag)

piece_checks = build_piece_checks(piece_types)

class Game:
    def __init__(self):
        self.board = {index: False for index in indices()}
        self.hand_size = 3
        self.hand = random.choices(piece_bag, k=self.hand_size)
        self.dead = False
        self.move_count = 0

    def randomize_board(self):
        self.board = {index: random.choice([True, False]) for index in indices()}

    def randomize_hand(self):
        self.hand = random.choices(piece_bag, k=self.hand_size)

    def random_play(self):
        try:
            move = random.choice(self.all_playable_moves())
            self.play_hand(*move)
        except IndexError:
            print("No possible moves!")
            self.dead = True

    def check_piece(self, piece, position):
        for hexagon in piece_hexes(piece, position):
            if hexagon not in self.board or self.board[hexagon]:
                return False

        return True

    def all_playable_moves(self):
        return [
            (piece_num, position)
            for position in indices()
            for piece_num, piece in enumerate(self.hand)
            if self.check_piece(piece, position)
        ]

    def place_piece(self, piece, position):
        for hexagon in piece_hexes(piece, position):
            self.board[hexagon] = True

    def play_hand(self, piece_num, position):
        piece = self.hand[piece_num]
        self.place_piece(piece, position)
        self.hand[piece_num] = random.choice(piece_bag)
        self.check_line_clears()
        self.move_count += 1



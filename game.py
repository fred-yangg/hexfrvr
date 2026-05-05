import random

from utils import indices

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
]

piece_types = set(piece_bag)

class Game:
    def __init__(self):
        self.board = {index: False for index in indices()}
        self.hand_size = 3
        self.hand = random.choices(piece_bag, k=self.hand_size)

    def randomize_board(self):
        self.board = {index: random.choice([True, False]) for index in indices()}

    def randomize_hand(self):
        self.hand = random.choices(piece_bag, k=self.hand_size)

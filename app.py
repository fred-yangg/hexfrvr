import math
import tkinter as tk

import strategies
from utils import indices

class Dimensions:
    def __init__(self, width, height, rows):
        self.width: int = width
        self.height: int = height
        self.rows: int = rows
        self.min_dim: int = min(self.width, self.height)
        self.major_radius: float = self.min_dim / (self.rows + 4) / 2
        self.minor_radius: float = self.major_radius * math.cos(math.radians(30))
        self.center_x: float = self.width / 2
        self.center_y: float = self.height / 2 - 4 * self.major_radius
        self.piece_centers: list[tuple[float, float]] = [
            (self.center_x / 3, self.center_y + 12 * self.major_radius),
            (self.center_x, self.center_y + 12 * self.major_radius),
            (self.center_x * 5 / 3, self.center_y + 12 * self.major_radius),
        ]

    # hex index to cartesian
    def h2c(self, index: tuple[float, float]):
        row, col = index
        x = (2 * col - row) * self.minor_radius
        y = 1.5 * row * self.major_radius
        return x, y


class HexGridTk(tk.Tk):
    def __init__(self, game, width=800, height=800, rows=9, coordinates_on=False, strategy=strategies.Random()):
        super().__init__()
        self.game = game
        self.title("Hex Grid")
        self.geometry(f'{width}x{height}')
        self.coordinates_on = coordinates_on
        self.strategy = strategy
        self.continuous_play = False

        self.grid_hexes: dict[tuple[int, int], int] = {index: 0 for index in indices()}
        self.hand_hexes: list[list[int]] = [[0 for _ in range(4)] for _ in range(self.game.hand_size)]

        self.bg_colour = '#4e4e6e'
        self.empty_colour = '#333333'
        self.cleared_colour = '#555555'
        self.placed_cleared_colour = '#556655'
        self.placed_colour = '#aaffaa'
        self.full_colour = '#ffffff'
        self.text_colour = '#7e7e9e'
        self.error_colour = '#ff0000'

        self.dim = Dimensions(width, height, rows)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=self.bg_colour, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.create_hexes()

        # Button to demonstrate fast color updates
        buttons = [
            tk.Button(self, text=f'Play Strategy "{self.strategy.name}"', command=self.make_play),
            tk.Button(self, text=f'Play Continuously', command=self.start_continuous_play),
            tk.Button(self, text="Reset", command=self.reset_game),
        ]

        for i, button in enumerate(buttons):
            button.place(x=20, y=20 + 40*i)

        self.dead_text = self.canvas.create_text(self.dim.center_x, self.dim.major_radius, text="", fill=self.error_colour, font=("Arial", 20, "bold"))

    def rerender(self):
        for index, filled in self.game.board.items():
            colour = self.full_colour if filled else self.empty_colour
            self.set_hex(index, colour)

        for piece_num, (piece, piece_hexes) in enumerate(zip(self.game.hand, self.hand_hexes)):
            hex_points = self.piece_hex_points(piece_num, piece)
            for hex_num, points in zip(piece_hexes, hex_points):
                self.canvas.coords(hex_num, *[coord for point in points for coord in point])

    def reset_game(self):
        self.game.reset()
        self.rerender()

    def make_play(self):
        prev_board = self.game.board.copy()
        move_played = self.game.play_strategy(self.strategy)

        # no move
        if not move_played:
            return

        # update hex grid
        for index in indices():
            prev_state = prev_board[index]
            curr_state = self.game.board[index]

            if curr_state == prev_state:
                if not curr_state:
                    self.set_hex(index, self.empty_colour)
                else:
                    self.set_hex(index, self.full_colour)
            elif not curr_state:
                self.set_hex(index, self.cleared_colour)

        # update specific play made
        for index in move_played:
            curr_state = self.game.board[index]

            if curr_state:
                self.set_hex(index, self.placed_colour)
            else:
                self.set_hex(index, self.placed_cleared_colour)

        # update hand
        for piece_num, (piece, piece_hexes) in enumerate(zip(self.game.hand, self.hand_hexes)):
            hex_points = self.piece_hex_points(piece_num, piece)
            for hex_num, points in zip(piece_hexes, hex_points):
                self.canvas.coords(hex_num, *[coord for point in points for coord in point])


    def start_continuous_play(self):
        self.continuous_play = True

    def set_hex(self, index, colour):
        hex_id = self.grid_hexes[index]
        self.canvas.itemconfig(hex_id, fill=colour)

    def hex_points(self, cx, cy) -> list[tuple[int, int]]:
        return [(
            cx + self.dim.major_radius * math.cos(math.radians(60 * i + 30)),
            cy + self.dim.major_radius * math.sin(math.radians(60 * i + 30))
        ) for i in range(6)]

    def piece_hex_points(self, piece_num, piece) -> list[list[tuple[float, float]]]:
        center_x, center_y = self.dim.piece_centers[piece_num]

        avg_x, avg_y = 0, 0
        for index in piece:
            x, y = self.dim.h2c(index)
            avg_x += x
            avg_y += y
        avg_x /= len(piece)
        avg_y /= len(piece)

        offset_x = center_x - avg_x
        offset_y = center_y - avg_y

        hex_points = []
        for hex_index in piece:
            cx, cy = self.dim.h2c(hex_index)
            cx += offset_x
            cy += offset_y
            hex_points.append(self.hex_points(cx, cy))

        return hex_points

    def create_hexes(self):
        # Hex Grid
        mid = (self.dim.rows - 1) / 2
        offset_x, offset_y = self.dim.h2c((mid, mid))
        offset_x = self.dim.center_x - offset_x
        offset_y = self.dim.center_y - offset_y
        for index in indices():
            row, col = index

            cx, cy = self.dim.h2c(index)
            cx += offset_x
            cy += offset_y

            points = self.hex_points(cx, cy)
            hex_id = self.canvas.create_polygon(points, outline=self.bg_colour, fill=self.empty_colour, width=3)
            self.grid_hexes[index] = hex_id
            if self.coordinates_on:
                self.canvas.create_text(cx, cy, text=f"{row},{col}", fill=self.text_colour, font=("Arial", 9, "bold"))

        # Pieces
        for piece_num, piece in enumerate(self.game.hand):
            hex_points = self.piece_hex_points(piece_num, piece)
            for hex_num, points in enumerate(hex_points):
                hex_id = self.canvas.create_polygon(points, outline=self.bg_colour, fill=self.full_colour, width=3)
                self.hand_hexes[piece_num][hex_num] = hex_id


    def update(self):
        if self.game.dead:
            self.canvas.itemconfig(self.dead_text, text=f"No possible moves after {self.game.move_count} moves!")
        else:
            self.canvas.itemconfig(self.dead_text, text=f"")

        if self.continuous_play:
            self.make_play()
            if self.game.dead:
                self.continuous_play = False

        super().update()
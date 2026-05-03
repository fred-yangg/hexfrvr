import math
import random
import tkinter as tk

from utils import indices

class Dimensions:
    def __init__(self, width, height, rows):
        self.width = width
        self.height = height
        self.rows = rows
        self.min_dim = min(self.width, self.height)
        self.major_radius = self.min_dim / (self.rows + 4) / 2
        self.minor_radius = self.major_radius * math.cos(math.radians(30))
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    # hex index to cartesian
    def h2c(self, index):
        row, col = index
        x = (2 * row - col) * self.minor_radius
        y = 1.5 * col * self.major_radius
        return x, y


class HexGridTk(tk.Tk):
    def __init__(self, game, width=800, height=800, rows=9):
        super().__init__()
        self.game = game
        self.title("Hex Grid")
        self.geometry(f'{width}x{height}')

        self.canvas_grid: dict[tuple[int, int], int] = {index: 0 for index in indices()}
        self.hand = []

        self.bg_colour = '#4e4e6e'
        self.empty_colour = '#333333'
        self.full_colour = '#ffffff'
        self.text_colour = '#7e7e9e'

        self.dim = Dimensions(width, height, rows)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=self.bg_colour, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.create_hex_grid()

        # Button to demonstrate fast color updates
        btn = tk.Button(self, text="Randomize All Colors", command=self.randomize_colors)
        btn.place(x=20, y=20)

    def randomize_colors(self):
        for hexagon in self.canvas_grid.values():
            self.canvas.itemconfig(hexagon, fill=random.choice([self.empty_colour, self.full_colour]))

    def set_hex(self, index, filled: bool):
        hex_id = self.canvas_grid[index]
        color = self.full_colour if filled else self.empty_colour
        self.canvas.itemconfig(hex_id, fill=color)

    def create_hex_grid(self):
        for row in range(9):
            row_size = 9 - abs(4 - row)
            start = 0 if row < 5 else row - 4
            cy = self.dim.center_y - (4 - row) * 1.5 * self.dim.major_radius

            for col in range(start, start + row_size):
                cx = self.dim.center_x - row_size * self.dim.minor_radius + (col - start) * self.dim.minor_radius * 2

                points = []
                for i in range(6):
                    angle = math.radians(60 * i + 30)
                    px = cx + self.dim.major_radius * math.cos(angle)
                    py = cy + self.dim.major_radius * math.sin(angle)
                    points.extend([px, py])

                hex_id = self.canvas.create_polygon(points, outline=self.bg_colour, fill=self.empty_colour, width=3)
                self.canvas_grid[(row, col)] = hex_id
                self.canvas.create_text(cx, cy, text=f"{row},{col}", fill=self.text_colour, font=("Arial", 9, "bold"))

    def update(self):
        for index, filled in self.game.board.items():
            self.set_hex(index, filled)

        super().update()
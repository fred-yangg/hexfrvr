from app import HexGridTk
from game import Game

if __name__ == "__main__":
    game = Game()
    app = HexGridTk(game)
    app.update()
    while True:
        # game.randomize_board()
        app.update()
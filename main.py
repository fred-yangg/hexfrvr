import strategies
from app import HexGridTk
from game import Game

if __name__ == "__main__":
    game = Game()
    app = HexGridTk(game, coordinates_on=True, strategy=strategies.EmptinessMaximization())
    app.update()
    while True:
        app.update()
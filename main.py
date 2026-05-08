import strategies
from app import HexGridTk
from game import Game

if __name__ == "__main__":
    game = Game()
    app = HexGridTk(
        game,
        coordinates_on=False,
        # strategy=strategies.Random(),
        # strategy=strategies.HexCounter(),
        # strategy=strategies.EmptinessMaximizationWithDotBias(),
        strategy=strategies.MoveMaximization(),
    )

    while True:
        app.update()
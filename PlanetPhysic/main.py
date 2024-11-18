import random
from src.physic import create_body, Coordinates
from src.physic.engine import System
from src.ui import Ui


if __name__ == "__main__":
    engine = System(0.01)
    renderer = Ui(engine , screen_size = (800, 600))
    for _ in range(50):
        engine.add_body(
            create_body(renderer.DIMENSION,
                        random.random() * 10,
                        random.random() * 10,
                        Coordinates.random(2, [(0, 800), (0, 600)]),
                        Coordinates.random(2, (-100, 100))
        ))
    renderer.run()

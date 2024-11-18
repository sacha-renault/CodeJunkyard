import random
import os
import json
from src.physic import create_body, Coordinates
from src.physic.engine import System
from src.ui import Ui


if __name__ == "__main__":
    # get path of this folder
    path = os.path.abspath(os.path.dirname(__file__))

    # create a system (engine)
    system = System(0.01)

    # create the object that will render
    renderer = Ui(system , screen_size = (800, 600), step_per_render=1, scale=2)

    # open the init.json
    with open(os.path.join(path, "init.json")) as file:
        objects: list[dict] = json.load(file)

    # for obj in objects:
    #     x = obj.get("x", renderer.screen_size[0] // 2)
    #     y = obj.get("y", renderer.screen_size[1] // 2)
    #     vx = obj.get("vx", 0)
    #     vy = obj.get("vy", 0)
    #     radius = obj.get("radius", 10)
    #     density = obj.get("density", 1)

    #     system.add_body(
    #         create_body(renderer.DIMENSION,
    #                     radius,
    #                     density,
    #                     Coordinates([x, y]),
    #                     Coordinates([vx, vy])
    #     ))
    for _ in range(50):
        system.add_body(
            create_body(renderer.DIMENSION,
                        random.random() * 10,
                        random.random() * 10,
                        Coordinates.random(2, [(0, 800), (0, 600)]),
                        Coordinates.random(2, (-100, 100))
        ))
    renderer.run()

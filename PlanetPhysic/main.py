from src.physic import Body, create_body, Coordinates
from src.physic.calculations import gravity_attraction, calculate_acc_array
from src.physic.engine import Engine
import random

if __name__ == "__main__":
    num_body = 20
    dimension = 2

    engine = Engine(0.0001)
    for _ in range(num_body):
        engine.add_body(
            create_body(
                dimension,
                random.random() * 10,
                1,
                Coordinates(
                    [(random.random() - 0.5) * 10_000 for _ in range(dimension)]
                )
        ))


    engine.run_n_step(1_000)
    for i, body in enumerate(engine.bodies):
        print(f"body{i}, {body.position=}, {body.speed=}")

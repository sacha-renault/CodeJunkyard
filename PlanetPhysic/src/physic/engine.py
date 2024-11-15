from typing import List

from .calculations import (calculate_acc_array, calculate_new_speed, calculate_new_position, get_collision)
from . import Body

class Engine:
    def __init__(self, dt: float) -> None:
        self.bodies: List[Body] = []
        self.frame_num = 0
        self.dt = dt

    def add_body(self, body: Body) -> None:
        if isinstance(body, Body):
            self.bodies.append(body)
        else:
            raise TypeError(f"body must be Body, not {type(body)}")

    def step(self) -> None:
        # increment frame
        self.frame_num += 1

        # calculate new acceleration and update bodies
        for body, acceleration in zip(self.bodies, calculate_acc_array(self.bodies), strict=True):
            body.acceleration = acceleration                        # acceleration updated at each step
            body.speed = calculate_new_speed(body, self.dt)         # speed updated at each step (before position)
            body.position = calculate_new_position(body, self.dt)   # position updated at each step

        # detect colision once position updated
        for idx1, idx2 in get_collision(self.bodies):
            pass
            # TODO
            # Do something for collision ?

    def run_n_step(self, n: int) -> None:
        for _ in range(n):
            self.step()
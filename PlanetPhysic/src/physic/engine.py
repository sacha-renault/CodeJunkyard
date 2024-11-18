from typing import List
import math
from .calculations import (calculate_acc_array, calculate_new_speed, calculate_new_position, get_collision)
from . import Body, create_body, sphere_volume

class System:
    def __init__(self, dt: float) -> None:
        self.bodies: List[Body] = []
        self.frame_num = 0
        self.dt = dt

    def add_body(self, body: Body) -> None:
        if isinstance(body, Body):
            self.bodies.append(body)
        else:
            raise TypeError(f"body must be Body, not {type(body)}")

    def _collision_handling(self) -> None:
        # create a set containing bodies that must be deleted
        body_to_remove = set()

        # detect colision before position update
        for idx1, idx2 in get_collision(self.bodies):
            # create a new planet that has volmue eq to sum of the two planet that collided
            body1 = self.bodies[idx1]
            body2 = self.bodies[idx2]
            v1 = sphere_volume(body1.radius)
            v2 = sphere_volume(body2.radius)
            new_radius = ((3 * (v1 + v2)) / (4 * math.pi)) ** (1/3)

            # Calculate total mass
            total_mass = body1.weight + body2.weight
            new_density = total_mass / sphere_volume(new_radius)

            # calc new position
            new_position = (body1.position + body2.position) / 2

            # calculate new speed
            new_speed = (body1.speed * body1.weight + body2.speed * body2.weight) / (2 * total_mass)

            # create a new body as fusion of the two previous
            new_body = create_body(body1.position.ndim, new_radius, new_density, new_position, new_speed)
            body_to_remove.add(body1)
            body_to_remove.add(body2)
            self.bodies.append(new_body)

        # now remove all after creating the new planets
        for body in body_to_remove:
            self.bodies.remove(body)

    def _update_positions(self) -> None:
        for body, acceleration in zip(self.bodies, calculate_acc_array(self.bodies), strict=True):
            body.acceleration = acceleration                        # acceleration updated at each step
            body.speed = calculate_new_speed(body, self.dt)         # speed updated at each step (before position)
            body.position = calculate_new_position(body, self.dt)   # position updated at each step

    def step(self) -> None:
        # increment frame
        self.frame_num += 1

        # collision
        self._collision_handling()

        # calculate new acceleration and update bodies
        self._update_positions()

    def run_n_step(self, n: int) -> None:
        for _ in range(n):
            self.step()
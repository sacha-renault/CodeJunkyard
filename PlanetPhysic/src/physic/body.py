from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math
from .coordinates import Coordinates

def sphere_volume(radius: float) -> float:
    return 4 / 3 * math.pi * math.pow(radius, 3)

def create_body(dimension: int,
                radius: float,
                density: float,
                inital_position: Optional[Coordinates] = None,
                inital_speed: Optional[Coordinates] = None,
                inital_acceleration: Optional[Coordinates] = None) -> Body:
    inital_position = inital_position if inital_position else Coordinates([0 for _ in range(dimension)])
    inital_speed = inital_speed if inital_speed else Coordinates([0 for _ in range(dimension)])
    inital_acceleration = inital_acceleration if inital_acceleration else Coordinates([0 for _ in range(dimension)])
    return Body(radius, density, inital_position, inital_speed, inital_acceleration)

@dataclass
class Body:
    radius: float
    density: float
    position: Coordinates
    speed: Coordinates
    acceleration: Coordinates

    def __post_init__(self) -> None:
        self.unique_id = id(self)

    def __hash__(self):
        return self.unique_id

    @property
    def weight(self) -> float:
        return sphere_volume(self.radius) * self.density
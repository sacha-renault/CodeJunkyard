from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math
from .coordinates import Coordinates

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

    @property
    def weight(self) -> float:
        return 4 / 3 * math.pi * math.pow(self.radius, 3) * self.density

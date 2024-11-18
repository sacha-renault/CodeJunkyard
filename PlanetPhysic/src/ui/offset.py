from typing import Tuple, Optional, Union
from enum import Enum, auto
from ..physic import Body

class Mode(Enum):
    FIXED = auto()
    FOLLOW = auto()

class Offset2D:
    def __init__(self, offset: Tuple[int, int], mode: str = Mode.FIXED, target: Optional[Body] = None):
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.mode = mode
        self.target = target

    @property
    def x(self) -> int:
        if self.mode == Mode.FIXED:
            return self.offset_x
        elif self.mode == Mode.FOLLOW and self.target is not None:
            return self.target.position[0]
        else:
            raise Exception("Mode is following but not target")

    @property
    def y(self) -> int:
        if self.mode == Mode.FIXED:
            return self.offset_y
        elif self.mode == Mode.FOLLOW and self.target is not None:
            return self.target.position[1]
        else:
            raise Exception("Mode is following but not target")

    def set(self, target_or_coordinates: Union[Body, Tuple[int, int], None]) -> None:
        if isinstance(target_or_coordinates, Body):
            self.mode = Mode.FOLLOW
            self.target = target_or_coordinates
        elif isinstance(target_or_coordinates, tuple):
            self.mode = Mode.FIXED
            self.offset_x = target_or_coordinates[0]
            self.offset_y = target_or_coordinates[1]
        elif target_or_coordinates is None:
            self.mode = Mode.FIXED
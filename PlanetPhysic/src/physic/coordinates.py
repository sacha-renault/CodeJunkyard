from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union, Callable, NamedTuple
import math
from .constant import Constant

# alias numeric
Numeric = Union[float, int]

# single operation
def addition(x: Numeric, y: Numeric) -> Numeric:
    return x + y

def subtraction(x: Numeric, y: Numeric) -> Numeric:
    return x - y

def multiplication(x: Numeric, y: Numeric) -> Numeric:
    return x * y

def division(x: Numeric, y: Numeric) -> Numeric:
    if abs(y) < Constant.EPSILON:
        if y >= 0:
            return x / Constant.EPSILON
        else:
            return - x / Constant.EPSILON
    return x / y

@dataclass
class Coordinates:
    coords: List[float]

    @property
    def ndim(self) -> int:
        return len(self.coords)

    def _operation(self, other: Union[Numeric, Coordinates], operation: Callable[[Numeric, Numeric], Numeric]) -> Coordinates:
        if isinstance(other, Numeric):
            return Coordinates([operation(coord, other) for coord in self.coords])
        elif isinstance(other, Coordinates):
            if self.ndim != other.ndim:
                raise TypeError(f"ndim must be equal for both points, found {self.ndim} and {other.ndim}")
            return Coordinates([operation(coord1, coord2) for coord1, coord2 in zip(self.coords, other.coords)])
        else:
            raise TypeError(f"other needs to be float, int or Point, not {type(other)}")

    def __add__(self, other: Union[Numeric, Coordinates]) -> Coordinates:
        return self._operation(other, addition)

    def __sub__(self, other: Union[Numeric, Coordinates]) -> Coordinates:
        return self._operation(other, subtraction)

    def __mul__(self, other: Union[Numeric, Coordinates]) -> Coordinates:
        return self._operation(other, multiplication)

    def __truediv__(self, other: Union[Numeric, Coordinates]) -> Coordinates:
        return self._operation(other, division)

if __name__ == "__main__":
    point = Coordinates([1, 1])
    print(point.magnitude_and_unit_vector(Coordinates([1, 1]) / Coordinates([1, 2])))
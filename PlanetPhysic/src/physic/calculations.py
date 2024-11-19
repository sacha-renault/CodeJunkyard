import math
from typing import NamedTuple, List, Tuple
from . import Coordinates
from .constant import Constant
from .body import Body

# Create an alias for DistanceOutput
class Vector(NamedTuple):
    magnitude: float
    unit_vector: Coordinates

def calculate_distance(coord1: Coordinates, coord2: Coordinates) -> float:
    difference_vector = coord2 - coord1
    return math.sqrt(sum(coord ** 2 for coord in difference_vector.coords))

def get_distance_as_vector(coord1: Coordinates, coord2: Coordinates) -> Vector:
    if coord1.ndim != coord2.ndim:
        raise TypeError(f"ndim must be equal for both points, found {coord1.ndim} and {coord2.ndim}")

    # Calculate the difference vector
    difference_vector = coord2 - coord1

    # Calculate the magnitude (Euclidean distance)
    magnitude = math.sqrt(sum(coord ** 2 for coord in difference_vector.coords))

    if magnitude < Constant.EPSILON:
        raise ValueError("Cannot normalize a zero vector.")

    # Normalize the direction vector to get the unit vector
    unit_vector = Coordinates([coord / magnitude for coord in difference_vector.coords])

    return Vector(magnitude, unit_vector)

def gravity_attraction(body1: Body, body2: Body) -> Vector:
    # get the distance
    magnitude, unit_vector = get_distance_as_vector(body1.position, body2.position)

    # calulate the magnitude of the force
    magnitude = Constant.G * body1.weight * body2.weight / math.pow(magnitude, 2)
    return Vector(magnitude, unit_vector)

def calculate_acc_array(bodies: List[Body]) -> List[Coordinates]:
    # init a list of null value for every body
    new_acc = [Coordinates([0 for _ in range(bodies[0].position.ndim)]) for _ in range(len(bodies))]

    # compute gravity attraction for all pair of planet
    for i, body1 in enumerate(bodies[:-1]):
        for j, body2 in enumerate(bodies[i+1:], start=i+1):
            magnitude, unit_vector = gravity_attraction(body1, body2)
            acc_vector = unit_vector * magnitude
            new_acc[i] += acc_vector / body1.weight
            new_acc[j] -= acc_vector / body2.weight

    return new_acc

def calculate_new_speed(body: Body, dt: float) -> Coordinates:
    return body.speed + body.acceleration * dt

def calculate_new_position(body: Body, dt: float) -> Coordinates:
    return body.position + body.speed * dt + body.acceleration * math.pow(dt, 2) * 0.5

def get_collision(bodies: List[Body]) -> List[Tuple[int, int]]:
    # init an empty list of collision
    body_collision = []

    # check for collision
    for i, body1 in enumerate(bodies[:-1]):
        for j, body2 in enumerate(bodies[i+1:], start=i+1):
            if calculate_distance(body1.position, body2.position) < body1.radius + body2.radius:
                body_collision.append((i, j))

    return body_collision

def as_vector(coordinates: Coordinates) -> Vector:
    # calculate magnitude
    magnitude = math.sqrt(sum(value ** 2 for value in coordinates.coords))

    # unit vector
    if magnitude == 0:
        unit_vector = Coordinates([0.0] * len(coordinates.coords))
    else:
        unit_vector = Coordinates([value / magnitude for value in coordinates.coords])

    return Vector(magnitude, unit_vector)
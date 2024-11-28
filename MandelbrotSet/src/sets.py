import numpy as np
from .calc import fc, complexArray

class ClassicSet:
    @property
    def aabb(self):
        return (-2, 1, -1.5, 1.5)

    @property
    def overflow_limit(self) -> int:
        return 1e5

    @property
    def max_iter(self) -> int:
        return 100

    def fc(self, z: complexArray, c: complexArray) -> complexArray:
        return fc(z, c)

class ExpSet(ClassicSet):
    @property
    def aabb(self):
        return (-200, 100, -150, 150)

    def fc(self, z: complexArray, c: complexArray) -> complexArray:
        return np.exp(z**(1/2)) + c

class SquareLogSet(ClassicSet):
    def fc(self, z, c):
        return z**2 + np.log(1 + z) + c

class SquareLogMeltedSet(ClassicSet):
    def fc(self, z, c):
        return z**2 + np.log(z + c) + c

    @property
    def aabb(self):
        return (-0.1, 0.9, -0.5, 0.5)

class ExpAddSet1(ClassicSet):
    def fc(self, z, c):
        root_c = c ** 0.5
        return z**2 + np.exp(root_c) * root_c

    @property
    def aabb(self):
        return (-2, 0.5, -1.25, 1.25)

class ExpAddSet2(ClassicSet):
    def fc(self, z, c):
        root_c = c ** 0.5
        return z**2 + np.exp(root_c)

    @property
    def aabb(self):
        return (-125, -5, -60, 60)

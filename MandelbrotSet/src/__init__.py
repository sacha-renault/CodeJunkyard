from typing import Tuple, Callable, Optional
import numpy as np

complexArray = np.ndarray[np.complex128]
maskArray = np.ndarray[int]

def initialize_grid(dimensions: Tuple[int, int],
                    real_min: float,
                    real_max: float,
                    complexe_min: Optional[float] = None,
                    complexe_max: Optional[float] = None) -> complexArray:
    # set up limit for complex
    complexe_min = complexe_min if complexe_min is not None else real_min
    complexe_max = complexe_max if complexe_max is not None else real_max

    # init empty grid
    grid = np.zeros(dimensions, dtype=np.complex128)

    # linspace for real
    grid += np.linspace(real_min, real_max, dimensions[0])

    # reverse linspace for imaginary numbers > we want decreasing over the y image
    grid += (1j * np.linspace(complexe_min, complexe_max, dimensions[1])).reshape((-1, 1))[::-1]

    return grid

def fc(z: complexArray, c: complexArray) -> complexArray:
    return z ** 2 + c

def mandelbrot(c: complexArray, max_iter: int, overflow_limit: float, fc: Callable[[complexArray], complexArray]) -> maskArray:
    z = np.zeros(c.shape, dtype=np.complex128)
    mask = np.zeros(c.shape, dtype=int)
    for i in range(max_iter):
        z = fc(z, c)
        overflow = np.abs(z) > overflow_limit
        mask[overflow & (mask == 0)] = i
        z[overflow] = 0
    mask[mask == 0] = max_iter
    return mask

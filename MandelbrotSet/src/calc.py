from typing import Tuple, Callable, Optional
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange

complexArray = np.ndarray[np.complex128]
maskArray = np.ndarray[int]
ComplexArrayFunction = Callable[[complexArray, complexArray], complexArray]

def initialize_grid(dimensions: Tuple[int, int],
                    real_min: float,
                    real_max: float,
                    complexe_min: Optional[float] = None,
                    complexe_max: Optional[float] = None) -> complexArray:
    """
    Initializes a 2D grid of complex numbers for Mandelbrot set computation.

    The grid spans the specified ranges for the real and imaginary parts of the complex numbers.
    If `complexe_min` or `complexe_max` are not provided, they default to `real_min` and `real_max`, respectively.

    Args:
        dimensions (Tuple[int, int]):
            The dimensions of the grid as (rows, columns). The number of rows corresponds
            to the resolution along the imaginary axis, and the number of columns corresponds
            to the resolution along the real axis.
        real_min (float):
            The minimum value of the real part of the complex numbers.
        real_max (float):
            The maximum value of the real part of the complex numbers.
        complexe_min (Optional[float], optional):
            The minimum value of the imaginary part of the complex numbers. Defaults to `real_min` if not provided.
        complexe_max (Optional[float], optional):
            The maximum value of the imaginary part of the complex numbers. Defaults to `real_max` if not provided.

    Returns:
        np.ndarray:
            A 2D array of complex numbers representing the grid. Each element is a complex number
            formed by combining the real and imaginary parts corresponding to the grid's position.
    """
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
    """basic mandelbrot function `fc`"""
    return z ** 2 + c

def mandelbrot(c: complexArray,
               max_iter: int,
               overflow_limit: float,
               fc: Callable[[complexArray], complexArray],
               use_tqdm: bool = False) -> maskArray:
    # z starts as 0
    z = np.zeros(c.shape, dtype=np.complex128)

    # init an empty mask
    mask = np.zeros(c.shape, dtype=int)

    #chose between tqdm and range
    iterable = trange(max_iter) if use_tqdm else range(max_iter)

    # loop to do all iterations
    for i in iterable:

        # calculate where current mask is 0
        null_mask = (mask == 0)

        # compute next z with provided function
        # compute only values that are non 0
        z[null_mask] = fc(z[null_mask], c[null_mask])

        # get a mask of overflowing values
        overflow = np.abs(z) > overflow_limit

        # all the value in the mask will be change to the step number
        mask[overflow & null_mask] = i

        # values that overflowed are changed to 0 (no need to recalculate)
        z[overflow] = 0

    # last calculation of where mask is 0
    mask[mask == 0] = max_iter

    return mask

def display_mandelbrot(grid_size: Tuple[int, int],
                       aabb: Tuple[float, float, float, float],
                       max_iter: int,
                       overflow_limit: float,
                       fc: Callable[[complexArray], complexArray],
                       use_tqdm: bool = False) -> None:
    # initialize the grid
    grid = initialize_grid(grid_size, *aabb)

    # compute an approx of mandlebrot set
    mask = mandelbrot(grid, max_iter, overflow_limit, fc, use_tqdm)

    # display
    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    ax.imshow(mask / np.max(mask), extent=aabb, cmap='hot')
    fig.tight_layout()
    plt.title("Mandelbrot Set")
    plt.show()

import os
import numpy as np
from scipy.signal import convolve2d

CONV_KER = np.ones((3,3))
CONV_KER[1,1] = 0

def next_step(grid: np.ndarray) -> np.ndarray:
    score: np.ndarray = convolve2d(grid, CONV_KER, mode="same")
    score3: np.ndarray = (score == 3)
    stay_alive: np.ndarray = (grid == 1) & (score3 | (score == 2))
    born: np.ndarray = (grid == 0) & score3
    return (stay_alive | born).astype(int)

def render_grid(grid: np.ndarray) -> None:
    assert len(grid.shape) == 2, "grid should be 2D"
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * (grid.shape[1] * 2 + 3))
    for row in grid:
        print("|", end = " ")
        for cell in row:
            print(" " if not cell else "o", end=" ")
        print("|")
    print("-" * (grid.shape[1] * 2 + 3))

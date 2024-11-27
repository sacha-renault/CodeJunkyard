import matplotlib.pyplot as plt
import numpy as np
from src import initialize_grid, mandelbrot, fc

if __name__ == "__main__":
    # parameters
    overflow_limit = 1e5
    max_iter = 500
    grid_size = 500
    aabb = (-2, 1, -1.5, 1.5)

    # computation
    grid = initialize_grid((grid_size, grid_size), *aabb)
    mask = mandelbrot(grid, max_iter, overflow_limit, fc)

    # display
    plt.imshow(mask / np.max(mask), extent=aabb, cmap='hot')
    plt.colorbar()
    plt.title("Mandelbrot Set")
    plt.show()

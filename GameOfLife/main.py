import numpy as np
from fpstimer import FPSTimer
from src import render_grid, next_step

if __name__ == "__main__":
    grid = np.random.randint(0, 2, (25,50))
    render_grid(grid)
    clock = FPSTimer(25)

    for _ in range(150):
        grid = next_step(grid)
        clock.sleep()
        render_grid(grid)
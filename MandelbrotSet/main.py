from src import display_mandelbrot

if __name__ == "__main__":
    # parameters
    overflow_limit = 1e5
    max_iter = 100
    grid_size = 750, 750
    aabb = (-2, 1, -1.5, 1.5)
    display_mandelbrot(grid_size, aabb, max_iter, overflow_limit)



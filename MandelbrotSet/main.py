from src import MandelbrotWindow

if __name__ == "__main__":
    # parameters
    overflow_limit = 1e5
    max_iter = 100
    grid_size = 800, 800
    aabb = (-2, 1, -1.5, 1.5)
    MandelbrotWindow(grid_size, aabb, overflow_limit, max_iter).root.mainloop()
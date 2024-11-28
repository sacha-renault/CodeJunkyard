from src import MandelbrotWindow
from src.sets import *


if __name__ == "__main__":
    # parameters
    grid_size = 800, 800

    # choose set to display
    dset = ExpAddSet2()

    # display
    win = MandelbrotWindow(grid_size, dset.aabb, dset.overflow_limit, dset.max_iter, dset.fc)
    win.root.mainloop()
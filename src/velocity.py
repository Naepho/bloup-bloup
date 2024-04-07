import numpy as np
from deriv import deriv

def velocity(psi_grid, nodes_num, nodes_dom, h):
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    horiz_speeds = np.zeros_like(psi_grid)
    vert_speeds = np.zeros_like(psi_grid)
    norm_speeds = np.zeros_like(psi_grid)

    for i in range(size_i):
        for j in range(size_j):
            if nodes_dom[i, j] == 0:
                continue

            horizontal_speed = -1 * deriv(psi_grid[i - 1, j], psi_grid[i, j], psi_grid[i + 1, j], \
                                          nodes_dom[i - 1, j], nodes_dom[i, j], nodes_dom[i + 1, j], \
                                          h)
            vertical_speed = deriv(psi_grid[i, j - 1], psi_grid[i, j], psi_grid[i, j + 1], \
                                   nodes_dom[i, j - 1], nodes_dom[i, j], nodes_dom[i, j + 1], \
                                   h)

            horiz_speeds[i, j] = horizontal_speed
            vert_speeds[i, j] = vertical_speed
            norm_speeds[i, j] = np.sqrt(horizontal_speed**2 + vertical_speed**2)

    return [horiz_speeds, vert_speeds, norm_speeds]

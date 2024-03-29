import numpy as np
import matplotlib.pyplot as plt

import solver
import speed

def displayPsi(psi, nodes_num):
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    grid = np.zeros((size_i, size_j))
    for i in range(size_i):
        for j in range(size_j):
            # For points outside of the region
            if (i == 0 or j == 0 or i == size_i - 1 or j == size_j - 1):
                grid[i][j] = 0
            # Gets the index of (i,j), and then puts its value in the grid
            # minus 1 because numerotation starts at 1
            else:
                index = nodes_num[i][j]
                grid[i][j] = psi[index - 1]
    return grid

if __name__=="__main__":
    flow_rate = (10 * 4 + 5 * 2) * 0.1
    print("Flow rate : " + str(flow_rate))
    island_cl = 3.2 # 3.2 is really good
    h = 2

    # Importing files
    path = "./files"
    nodes_num = np.loadtxt(path + '/' + "4-num.txt", dtype = int)
    nodes_dom = np.loadtxt(path + '/' + "4-dom.txt", dtype = int)
#     nodes_cl = np.loadtxt(path + '/' + "1-cl.txt", dtype = float)

    # Creating boundary conditions
    nodes_cl = solver.createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl)

    A, b = solver.createSystem(nodes_num, nodes_dom, nodes_cl)
    A = A.tocsr()
    psi = solver.solve_syst(A, b)

    psi_grid = displayPsi(psi, nodes_num)
    # grid = np.rot90(grid, 1)

    horiz_speeds, vert_speeds, norm_speeds = speed.getSpeed(psi_grid, nodes_num, nodes_dom, h)
    print("Max speed : " + str(norm_speeds.max()))

    flow_rate_computed = 0
    for i in vert_speeds[1]:
        flow_rate_computed += i*h # Because h = 2

    print(flow_rate_computed)

    plt.imshow(norm_speeds)
    plt.show()

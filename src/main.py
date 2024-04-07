import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import newton

import solver
import velocity
import pressure
import circu
import force

def displayPsi(psi, nodes_num, nodes_dom):
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    grid = np.zeros((size_i, size_j))
    for i in range(size_i):
        for j in range(size_j):
            # For points outside of the region
            if (nodes_dom[i, j] == 0):
                grid[i][j] = 0
            # Gets the index of (i,j), and then puts its value in the grid
            # minus 1 because numerotation starts at 1
            else:
                index = nodes_num[i][j]
                grid[i][j] = psi[index - 1]
    return grid

def optimize_circu(goal, initial_guess):
    path = "./files"
    nodes_num = np.loadtxt(path + '/' + "4-num.txt", dtype = int)
    nodes_dom = np.loadtxt(path + '/' + "4-dom.txt", dtype = int)
    contourObj = np.loadtxt(path + '/' + "4-contourObj.txt", dtype = int)
    x = contourObj[:, 0]
    y = contourObj[:, 1]

    solution = newton(lambda k: solveOptimize(5, k, 2, nodes_num, nodes_dom, x, y, goal), initial_guess)
    return solution

def solveOptimize(flow_rate, island_cl, h, nodes_num, nodes_dom, x, y, goal):
    nodes_cl = solver.createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl)

    A, b = solver.createSystem(nodes_num, nodes_dom, nodes_cl)
    A = A.tocsr()
    psi = solver.solve_syst(A, b)

    psi_grid = displayPsi(psi, nodes_num, nodes_dom)

    horiz_speeds, vert_speeds, norm_speeds = velocity.velocity(psi_grid, nodes_num, nodes_dom, h)
    x = [0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4, 2, 0, 0, 0, 0, 0, 0]
    y = [0, 0, 0, 0, 0, 0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4, 2, 0]
    for i in range(len(x)):
        x[i] += 300
        y[i] += 35

    u = np.zeros_like(x, dtype = float)
    v = np.zeros_like(y, dtype = float)
    for i in range(len(x)):
        u[i] = horiz_speeds[x[i], y[i]]
        v[i] = vert_speeds[x[i], y[i]]

    c = circu.circu(u, v, x, y)

    max_speed = norm_speeds.max()
    mean_speed = norm_speeds.mean()

    pressures = pressure.pressure(norm_speeds)

    return (c - goal)

if __name__=="__main__":
    start_time = time.time()
    flow_rate = (10 * 4 + 5 * 2) * 0.1
    print("Flow rate : " + str(flow_rate))
    island_cl = 3.2 # 3.2 is really good
    island_cl = optimize_circu(0, 0)
    print("Optimal island_cl : " + str(island_cl))
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

    psi_grid = displayPsi(psi, nodes_num, nodes_dom)

    horiz_speeds, vert_speeds, norm_speeds = velocity.velocity(psi_grid, nodes_num, nodes_dom, h)
    print("Max speed : " + str(norm_speeds.max()))
    print("Mean speed : " + str(norm_speeds.mean()))

    flow_rate_computed = 0
    for i in vert_speeds[1]:
        flow_rate_computed += i*h # Because h = 2

    print("Computed flow rate : " + str(flow_rate_computed))
    # norm_speeds = np.rot90(norm_speeds, 1)
    # norm_speeds = np.flip(norm_speeds, 0)
    pressures = pressure.pressure(norm_speeds)

    plt.subplot(1, 3, 1)
    plt.imshow(norm_speeds, cmap="magma")
    plt.title("Norme de la vitesse")
    plt.subplot(1, 3, 3)
    plt.imshow(psi_grid, cmap="magma")
    plt.title("Fonction de courant")
    plt.subplot(1, 3, 2)
    plt.imshow(pressures, cmap="magma")
    plt.title("Pression")

    x = [0, 2, 4, 4, 4, 2, 0, 0, 0]
    y = [0, 0, 0, 2, 4, 4, 4, 2, 0]
    # contourObj = np.loadtxt(path + '/' + "4-contourObj.txt", dtype = int)
    # x = contourObj[:, 0]
    # y = contourObj[:, 1]
    for i in range(len(x)):
        x[i] += 275
        y[i] += 25
    u = np.zeros_like(x, dtype = float)
    v = np.zeros_like(y, dtype = float)
    p = np.zeros_like(x)
    for i in range(len(x)):
        u[i] = horiz_speeds[x[i], y[i]]
        v[i] = vert_speeds[x[i], y[i]]
        p[i] = pressures[x[i], y[i]]

    c = circu.circu(u, v, x, y)
    fx, fy = force.force(p, x, y)
    print("Circulation : " + str(c))
    print("Force : "+ str(fx) + " " + str(fy))

    print(time.time() - start_time)
    plt.show()

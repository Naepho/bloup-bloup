import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import newton

import solver
import velocity
import pressure
import circu
import force

def optimize(goal, initial_guess, nodes_num, nodes_dom, x, y):
    """
    Fonction pour trouver des valeurs optimales pour la condition limite de l'îlot
    """

    solution = newton(lambda k: solveOptimize(5, k, 2, nodes_num, nodes_dom, x, y, goal), initial_guess, tol=1e-17)
    return solution

def solveOptimize(flow_rate, island_cl, h, nodes_num, nodes_dom, x, y, goal):
    """
    Résolution du Laplacien pour l'optimisation
    """

    nodes_cl = solver.createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl)

    psi_grid = solver.solve_syst(nodes_num, nodes_dom, None, flow_rate, island_cl)

    horiz_speeds, vert_speeds, norm_speeds = velocity.velocity(psi_grid, nodes_num, nodes_dom, h)

    u = np.zeros_like(x, dtype = float)
    v = np.zeros_like(y, dtype = float)
    p = np.zeros_like(x, dtype = float)
    for i in range(len(x)):
        u[i] = horiz_speeds[int(x[i]), int(y[i])]
        v[i] = vert_speeds[int(x[i]), int(y[i])]

    c = circu.circu(u, v, x, y)

    max_speed = norm_speeds.max()
    mean_speed = norm_speeds.mean()

    pressures = pressure.pressure(norm_speeds)

    return (pressures[10][350] - pressures[85][350] - goal)

if __name__=="__main__":
    start_time = time.time()

    flow_rate = (10 * 4 + 5 * 2) * 0.1
    print("Flow rate : " + str(flow_rate))

    ## Obtention des variables dépendantes du cas
    case = 4

    if case == 1:
        h = 0.5

        path = "./files"
        nodes_num = np.loadtxt(path + '/' + "1-num.txt", dtype = int)
        nodes_num = np.rot90(nodes_num, 1)
        nodes_dom = np.loadtxt(path + '/' + "1-dom.txt", dtype = int)
        nodes_dom = np.rot90(nodes_dom, 1)
        nodes_cl = np.loadtxt(path + '/' + "1-cl.txt", dtype = float)
        nodes_cl = np.rot90(nodes_cl, 1)

        ## La circulation et les forces ne sont pas nécessaires
        island_cl = None

    if case == 2:
        h = 2

        path = "./files"
        nodes_num = np.loadtxt(path + '/' + "2-num.txt", dtype = int)
        nodes_num = np.rot90(nodes_num, 1)
        nodes_dom = np.loadtxt(path + '/' + "2-dom.txt", dtype = int)
        nodes_dom = np.rot90(nodes_dom, 1)
        nodes_cl = None

        island_cl = 2.5
        size_of_perimeter = (72 - 43) * 2 + (453 - 268) * 2
        x = np.zeros(size_of_perimeter + 1)
        y = np.zeros(size_of_perimeter + 1)

        count = 0
        for i in range(43, 72):
            x[count] = i
            y[count] = 268
            count += 1
        for i in range(268, 453):
            x[count] = 72
            y[count] = i
            count += 1
        for i in range(72, 43, -1):
            x[count] = i
            y[count] = 453
            count += 1
        for i in range(453, 268, -1):
            x[count] = 43
            y[count] = i
            count += 1
        x[-1] = 43
        y[-1] = 268

    if case == 3:
        h = 2

        path = "./files"
        nodes_num = np.loadtxt(path + '/' + "3-num.txt", dtype = int)
        nodes_num = np.rot90(nodes_num, 1)
        nodes_dom = np.loadtxt(path + '/' + "3-dom.txt", dtype = int)
        nodes_dom = np.rot90(nodes_dom, 1)
        nodes_cl = None

        size_of_perimeter = (86 - 62) * 2 + (451 - 271) * 2
        x = np.zeros(size_of_perimeter + 1)
        y = np.zeros(size_of_perimeter + 1)

        count = 0
        for i in range(62, 86):
            x[count] = i
            y[count] = 271
            count += 1
        for i in range(271, 451):
            x[count] = 86
            y[count] = i
            count += 1
        for i in range(86, 62, -1):
            x[count] = i
            y[count] = 451
            count += 1
        for i in range(451, 271, -1):
            x[count] = 62
            y[count] = i
            count += 1
        x[-1] = 62
        y[-1] = 271

        island_cl = 2.5

    if case == 4:
        h = 2

        path = "./files"
        nodes_num = np.loadtxt(path + '/' + "4-num.txt", dtype = int)
        nodes_num = np.rot90(nodes_num, 1)
        nodes_dom = np.loadtxt(path + '/' + "4-dom.txt", dtype = int)
        nodes_dom = np.rot90(nodes_dom, 1)
        nodes_cl = None

        island_cl = 1.765026457295446872

        contourObj = np.loadtxt(path + '/' + "4-contourObj.txt", dtype = np.double)
        x = contourObj[:, 1]
        y = contourObj[:, 0]

    ## Résolution générale

    psi_grid = solver.solve_syst(nodes_num, nodes_dom, nodes_cl, flow_rate, island_cl)

    horiz_speeds, vert_speeds, norm_speeds = velocity.velocity(psi_grid, nodes_num, nodes_dom, h)
    print("Max speed : " + str(norm_speeds.max()))
    print("Mean speed : " + str(norm_speeds.mean()))

    flow_rate_computed = 0
    for i in horiz_speeds[:, 350]:
        flow_rate_computed += i*h
    print("Computed flow rate : " + str(flow_rate_computed))

    pressures = pressure.pressure(norm_speeds)

    ## Création du graphique

    plt.figure(figsize = (10, 10), dpi = 100)
    plt.tight_layout()

    plt.subplot(3, 1, 1)
    im1 = plt.imshow(norm_speeds[1:-2, 1:-2], cmap="magma")
    plt.title("Norme de la vitesse")
    plt.colorbar(im1, ax = plt.gca(), shrink = 0.75)

    plt.subplot(3, 1, 3)
    im2 = plt.imshow(psi_grid[1:-2, 1:-2], cmap="magma")
    plt.title("Fonction de courant")
    plt.colorbar(im2, ax = plt.gca(), shrink = 0.75)

    x_m = np.arange(0, horiz_speeds.shape[1], dtype = np.double)
    y_m = np.arange(0, horiz_speeds.shape[0], dtype = np.double)
    X, Y = np.meshgrid(x_m, y_m)
    # Tracer les lignes de courant avec streamplot
    horiz_speeds = np.array(horiz_speeds, dtype = np.double)
    vert_speeds = np.array(vert_speeds, dtype = np.double)
    plt.streamplot(X, Y, horiz_speeds, vert_speeds, color='lightblue', linewidth=1, arrowsize=0, density=0.5)

    plt.subplot(3, 1, 2)
    im3 = plt.imshow(pressures[1:-2, 1:-2], cmap="magma")
    plt.title("Pression")
    plt.colorbar(im3, ax = plt.gca(), shrink = 0.75)


    ## Calcul des forces et de la circulation uniquement s'il y a un îlot
    if case != 1:
        u = np.zeros_like(x, dtype = float)
        v = np.zeros_like(y, dtype = float)
        p = np.zeros_like(x, dtype = float)
        for i in range(len(x)):
            u[i] = horiz_speeds[int(x[i]), int(y[i])]
            v[i] = vert_speeds[int(x[i]), int(y[i])]
            p[i] = pressures[int(x[i]), int(y[i])]

        c = circu.circu(u, v, x, y)
        fx, fy = force.force(p, x, y)
        print("Circulation : " + str(c))
        print("Force : fx = "+ str(fx) + " ; fy = " + str(fy))

    print("Time to run : " + str(time.time() - start_time))
    plt.show()

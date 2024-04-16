## Imports
import numpy as np
from scipy import sparse as sp
import matplotlib.pyplot as plt
from getCoeff import getCoeff

## Ajusting the output grid
def displayPsi(psi, nodes_num, nodes_dom):
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    grid = np.zeros((size_i, size_j), dtype = np.longdouble)
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


## Boundary conditions

def createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl):
    """
    Creates a matrix for boundary condtions using nodes_num and nodes_cl
    Returns nodes_cl
    """

    # Creating the matrix
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])
    nodes_cl = np.zeros((size_i, size_j), dtype = np.longdouble)

    # Setting the values
    for i in range(size_i):
        for j in range(size_j):
            if nodes_dom[i, j] == 0:
                continue
            elif nodes_dom[i , j] == 1:
                continue
            elif nodes_dom[i, j] == 2:
                # First, if at the border
                # psi has to be linear at the beginning and same values at the end
                # Constant around the borders
                if (j == 1 or j == size_j - 2):
                    nodes_cl[i, j] = flow_rate * (i) / (size_i - 2)
                elif i == 1:
                    nodes_cl[i, j] = flow_rate / (size_i - 2)
                elif i == size_i - 2:
                    nodes_cl[i, j] = flow_rate

                # Second, for the island
                else:
                    nodes_cl[i, j] = island_cl

                nodes_cl[i, j] -= flow_rate / (size_i - 2)

            else:
                continue


    return nodes_cl

## Making system

def createSystem(nodes_num, nodes_dom, nodes_cl):
    """
    Function that builds the system to be solved.
    Takes as input :
    - <path> : the path of the files containing information
    - <num> : the name of the file with the numerotation of the points
    - <dom> : the name of the file with the types of the points
    - [cl] : the name of the file with the limit conditions
    Returns the matrix A and the vector b
    """

    # Getting the number of elements to solve in the matrix
    # size = np.count_nonzero(nodes_num)
    size = np.max(nodes_num)
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    # Creating A and B
    A = sp.lil_matrix((size, size), dtype = np.double)
    B = np.zeros((size), dtype = np.double)

    # Making it work
    for i in range(size_i):
        for j in range(size_j):
            if nodes_dom[i, j] == 0:
                continue

            n, a, b = getCoeff(nodes_num[i, j - 1], nodes_num[i, j + 1], \
                               nodes_num[i - 1, j], nodes_num[i + 1, j], \
                               nodes_num[i, j], nodes_dom[i, j], nodes_cl[i, j])

            if type(a) == int and a == 0:
                continue
            else:
                k = nodes_num[i, j]
                for p in range(len(n)):
                    A[k - 1, n[p] - 1] = a[p]
                B[k - 1] = b

    return [A, B]

def solve_syst(nodes_num, nodes_dom, nodes_cl, flow_rate, island_cl):
    """
    Solves the system.
    Is shorter to write
    """

    if type(nodes_cl) != "NoneType":
        nodes_cl = createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl)
    A, b = createSystem(nodes_num, nodes_dom, nodes_cl)
    A = A.tocsr()
    x = sp.linalg.spsolve(A,b)
    grid = displayPsi(x, nodes_num, nodes_dom)
    return grid

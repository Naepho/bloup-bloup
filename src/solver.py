## Imports
import numpy as np
from scipy import sparse as sp
import matplotlib.pyplot as plt
from getCoeff import getCoeff

## Boundary conditions

def createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl):
    """
    Creates a matrix for boundary condtions using nodes_num and nodes_cl
    Returns nodes_cl
    """

    # Creating the matrix
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])
    nodes_cl = np.zeros((size_i, size_j))

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
                if (i == 1 or i == size_i - 2):
                    nodes_cl[i, j] = flow_rate * (j) / (size_j - 2)
                elif j == 1:
                    nodes_cl[i, j] = flow_rate / (size_j - 2)
                elif j == size_j - 2:
                    nodes_cl[i, j] = flow_rate

                # Second, for the island
                else:
                    nodes_cl[i, j] = island_cl

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
    A = sp.lil_matrix((size, size))
    B = np.zeros((size))

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

def solve_syst(A, b):
    """
    Solves the system.
    Is shorter to write
    """
    x = sp.linalg.spsolve(A,b)
    return x

if __name__=="__main__":
    # Import file into matrix
    path = "."
    nodes_num = np.loadtxt(path + '/' + "1-num.txt", dtype = int)
    nodes_dom = np.loadtxt(path + '/' + "1-dom.txt", dtype = int)
    nodes_cl = np.loadtxt(path + '/' + "1-cl.txt", dtype = float)

    # Creating the system
    A, b = createSystem(nodes_num, nodes_dom, nodes_cl)

    # Loads the numerotation, and gets the size of the side of the whole problem
    nodes_num = np.loadtxt("./1-num.txt", dtype = int)
    size = len(nodes_num)
    
    # Transforms A for solving, and solves
    A = A.tocsr()
    x = solve_syst(A, b)

    # Maps the solution to the grid of the problem
    grid = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            # For points outside of the region
            if (i == 0 or j == 0 or i == size - 1 or j == size - 1):
                grid[i][j] = 0
            # Gets the index of (i,j), and then puts its value in the grid
            # minus 1 because numerotation starts at 1
            else:
                index = nodes_num[i][j]
                grid[i][j] = x[index - 1]
    print(grid)
    plt.imshow(grid)
    plt.show()

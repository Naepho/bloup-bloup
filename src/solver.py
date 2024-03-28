## Imports
import numpy as np
from scipy import sparse as sp
import matplotlib.pyplot as plt

## Making system

def getCoeff(num_left, num_right, num_down, num_up, num_cent, type_cent, cl_cent):
    """
    This function returns the values to be put inside A and b given parameters.
    For more details, see the project statement.
    """

    # If, for some reason, we get something outside of the simulation
    if type_cent == 0:
        a = np.array([0])
        j = a
        b = 0

    # Node inside the simulation
    elif type_cent == 1:
        a = np.array([1, 1, 1, 1, -4])
        j = np.array([num_left, num_right, num_down, num_up, num_cent])
        b = 0

    # Node at the limit
    elif type_cent == 2:
        a = np.array([1])
        j = np.array([num_cent])
        b = cl_cent

    # Failsafe
    else:
        a = 0
        j = 0
        b = 0

    return [j, a, b]

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
    # Creates matrix and vector, and gets size of the side of the region
    # minus 2 because we don't need the zeros on the border
    size = len(nodes_num) - 2
    A = sp.lil_matrix(((size)**2, (size)**2))
    B = np.zeros(((size)**2))

    # Gets the coefficients for each cell in the region and puts them in A and b
    # +1 in getCoeff because in nodes_num and nodes_dom, there's the first lines of 0
    for i in range(size):
        for j in range(size):
            n, a, b = getCoeff(nodes_num[(i + 1)][(j + 1) - 1], nodes_num[(i + 1)][(j + 1) + 1], \
                               nodes_num[(i + 1) - 1][(j + 1)], nodes_num[(i + 1) + 1][(j + 1)], \
                               nodes_num[(i + 1)][(j + 1)], nodes_dom[(i + 1)][(j + 1)], \
                               nodes_cl[(i + 1)][(j + 1)])

            # Continues if outside of the region
            if type(a) == int and a == 0:
                continue
            # Puts the coefficients in A and b
            # In getCoeff, it's j but here it's n because j was already taken by the loop
            # n[k] - 1 because the numerotation starts at 1 in n
            else:
                for k in range(len(n)):
                    A[i * (size) + j, n[k] - 1] = a[k]
                B[i * (size) + j] = b

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

import numpy as np

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

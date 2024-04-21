import numpy as np

def getCoeff(num_left, num_right, num_down, num_up, num_cent, type_cent, cl_cent):
    """
    Création des coefficients pour la résolution du système.
    """

    # Cas en dehors du domaine
    if type_cent == 0:
        a = np.array([0])
        j = a
        b = 0

    # Noeud dans la résolution
    elif type_cent == 1:
        a = np.array([1, 1, 1, 1, -4]).T
        j = np.array([num_left, num_right, num_down, num_up, num_cent]).T
        b = 0

    # Noeud limite
    elif type_cent == 2:
        a = np.array([1])
        j = np.array([num_cent])
        b = cl_cent

    # Au cas où
    else:
        a = 0
        j = 0
        b = 0

    return [j, a, b]

## Imports
import numpy as np
from scipy import sparse as sp
import matplotlib.pyplot as plt
from getCoeff import getCoeff

def displayPsi(psi, nodes_num, nodes_dom):
    """
    Fonction pour mapper le vecteur des psi sur la grille des noeuds
    """

    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    grid = np.zeros((size_i, size_j), dtype = np.longdouble)
    for i in range(size_i):
        for j in range(size_j):
            # Pour les points en dehors de la région
            if (nodes_dom[i, j] == 0):
                grid[i][j] = 0

            # Obtention de la valeur de l'index de (i,j)
            # Le -1 est là car la numérotation commence à 1
            else:
                index = nodes_num[i][j]
                grid[i][j] = psi[index - 1]
    return grid

def createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl):
    """
    Crée une matrice pour les conditions limites
    """

    # Initialisation de la matrice
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])
    nodes_cl = np.zeros((size_i, size_j), dtype = np.longdouble)

    # Valeurs
    for i in range(size_i):
        for j in range(size_j):
            if nodes_dom[i, j] == 0:
                continue
            elif nodes_dom[i , j] == 1:
                continue
            elif nodes_dom[i, j] == 2:
                # Premièrement, la limite du domaine
                # Psi doit être linéaire au début et à la fin
                # Et constant sur les bords
                if (j == 1 or j == size_j - 2):
                    nodes_cl[i, j] = flow_rate * (i) / (size_i - 2)
                elif i == 1:
                    nodes_cl[i, j] = flow_rate / (size_i - 2)
                elif i == size_i - 2:
                    nodes_cl[i, j] = flow_rate

                # Deuxièmement, l'îlot
                else:
                    nodes_cl[i, j] = island_cl

                # Pour commencer à zéro. Ne change rien vu que psi se fait dériver.
                nodes_cl[i, j] -= flow_rate / (size_i - 2)

            else:
                continue


    return nodes_cl

def createSystem(nodes_num, nodes_dom, nodes_cl):
    """
    Fonction qui crée le système à résoudre
    """

    # Variables nécessaires
    size = np.max(nodes_num)
    size_i = len(nodes_num)
    size_j = len(nodes_num[0])

    # Initialisation de A et b
    A = sp.lil_matrix((size, size), dtype = np.double)
    B = np.zeros((size), dtype = np.double)

    # Assignation des valeurs
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
    Résolution du problème sur base des variables données
    """

    if type(island_cl) != "NoneType":
        nodes_cl = createBoundaryConditions(nodes_num, nodes_dom, flow_rate, island_cl)
    A, b = createSystem(nodes_num, nodes_dom, nodes_cl)
    A = A.tocsr()
    x = sp.linalg.spsolve(A,b)
    grid = displayPsi(x, nodes_num, nodes_dom)
    return grid

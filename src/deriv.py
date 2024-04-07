import numpy as np

def deriv(f_left, f_c, f_right, type_left, type_c, type_right, h):
    """
    Les vitesses sont calculées comme la dérivée de la fonction de courant. Il vous est demandé de coder une fonction qui permet de calculer la dérivée en un nœud du domaine. Etant donné la présence de limites dans le domaine, la dérivée devra tantôt être calculée centrée, tantôt décentrée. La fonction que vous écrirez doit prendre cet aspect en considération. L'interface de la fonction doit être deriv(f_left, f_c, f_right, type_left, type_c, type_right, h) et retourner v, avec:

    f_xxx la valeur de la fonction à dériver à gauche, au centre et à droite, respectivement en bas, au centre et en haut
    type_xxx le type de nœud (0 = hors domaine de calcul, 1 = nœud de calcul entouré de nœuds de calcul ou condition limite et 2 = nœud condition limite de Dirichlet) à gauche, au centre et à droite, respectivement en bas, au centre et en haut
    h le pas spatial entre deux nœuds
    v la valeur numérique de la dérivée
    """
    if (type_c == 0 or h == 0):
        print("Erreur: c = ",type_c, " et h = ", h)
        return 0
    elif type_left == 0:
        return (f_right-f_c)/h
    elif type_right == 0:
        return (f_c-f_left)/h
    else:
        return (f_right-f_left)/(2*h)


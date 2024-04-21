import numpy as np

def deriv(f_left, f_c, f_right, type_left, type_c, type_right, h):
    """
    La dérivée dans le cas général n'est pas centrée.
    Suite à un conseil du professeur Pirotton, nous avons fait cela.
    La justification derrière est que les coefficients utilisés pour résoudre le système sont basés sur une telle dérivée, et donc calculer une dérivée centrée peut créer des erreurs de calculs.
    La dérivée centrée est de toute façon juste en dessous, commentée.
    """
    if (type_c == 0 or h == 0):
        return 0
    elif type_left == 0:
        return (f_right - f_c)/h
    elif type_right == 0:
        return (f_c - f_left)/h
    else:
        return (f_right - f_c) / h
#       return (f_right - f_left) / (2 * h)

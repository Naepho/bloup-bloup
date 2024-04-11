import numpy as np

def circu(u, v, x, y):
    length = len(x) - 1
    c = 0

    for i in range(length):
        delta_x = x[i + 1] - x[i]
        delta_y = y[i + 1] - y[i]
        speed_x = u[i]
        speed_y = v[i]

        c += delta_x * speed_x + delta_y * speed_y
        print("temp circ : " + str(c))

    return c

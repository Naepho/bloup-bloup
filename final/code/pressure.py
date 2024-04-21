import numpy as np

def pressure(speed):
    p = np.zeros_like(speed)
    size_i = len(speed)
    size_j = len(speed[0])

    for i in range(size_i):
        for j in range(size_j):
            p[i][j] = -1 * speed[i][j]**2 * 1000 / 2

    p_min = np.abs(p.min())
    p += p_min * np.ones_like(p) * 2
    
    return p

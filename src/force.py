import numpy as np

def force(p,x,y):
    f = np.zeros(2)
    length = len(p) - 1

    for i in range(length):
        pos = np.array([x[i + 1] - x[i], y[i + 1] - y[i]])
        # fx += (p[i]+p[i+1])*(x[i+1]-x[i])/2
        # fy += (p[i]+p[i+1])*(y[i+1]-y[i])/2
        f += (p[i + 1] + p[i]) * pos / 2

    return f[0], f[1]

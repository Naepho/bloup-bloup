import numpy as np

def circu(u, v, x, y):
    length = len(x) - 1

    c = 0
    for i in range(length):
        pos = np.array([x[i + 1] - x[i], y[i + 1] - y[i]])
        speed_1 = np.array([u[i], v[i]])
        speed_2 = np.array([u[i + 1], v[i + 1]])

        mean_speed = (speed_1 + speed_2) / 2
        c += np.dot(mean_speed, pos)
        print("temp circ at i = " + str(i) + " with c = " + str(c))
        print("\t mean_speed : " + str(mean_speed) + " and pos : " + str(pos))

    return c

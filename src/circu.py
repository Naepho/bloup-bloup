import numpy as np

# def circu(u, v, x, y):
#     length = len(x) - 1
#     c = 0

#     for i in range(length):
#         print("coordinates : (" + str(x[i]) + ";" + str(y[i]) + ")")
#         print("next coordinated : (" + str(x[i + 1]) + ";" + str(y[i + 1]) + ")")
#         delta_x = x[i + 1] - x[i]
#         print("Delta x : " + str(delta_x))
#         delta_y = y[i + 1] - y[i]
#         print("Delta y : " + str(delta_y))
#         speed_x = u[i + 1] + u[i]
#         print("speed_x : " + str(speed_x))
#         speed_y = v[i] + v[i + 1]
#         print("speed_y : " + str(speed_y))

#         c += delta_x * speed_x/2 + delta_y * speed_y / 2
#         print("added : " + str(delta_x * speed_x + delta_y * speed_y))
#         print("temp circ : " + str(c))
#         print("-----")

#     print("=======")
#     return c
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

    return c

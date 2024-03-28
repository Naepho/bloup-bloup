import numpy as np
import matplotlib.pyplot as plt

import solver

if __name__=="__main__":
    # Importing files
    path = "./files"
    nodes_num = np.loadtxt(path + '/' + "2-num.txt", dtype = int)
    nodes_dom = np.loadtxt(path + '/' + "2-dom.txt", dtype = int)
    nodes_cl = np.loadtxt(path + '/' + "1-cl.txt", dtype = float)

    plt.imshow(nodes_dom)
    plt.show()

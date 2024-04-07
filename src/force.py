def force(p,x,y):
    fx, fy = 0 , 0

    for i in range(len(p) -1):
        fx += (p[i]+p[i+1])*(y[i+1]-y[i])/2
        fy += -1 * (p[i]+p[i+1])*(x[i+1]-x[i])/2

    return fx, fy

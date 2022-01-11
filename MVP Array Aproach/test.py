# import numpy as np
import numpy as np

"""

Particles:
    0 pos x
    1 pos y
    2 acc x
    3 acc y
    4 p_pos x
    5 p_pos y
    6 vel x
    7 vel y
    8 mass 

    p[...,0:2] : pos
    p[...,2:4] : acc
    p[...,4:6] : p_pos
    p[...,6:8] : vel
    p[...,8] : m


Springs:
    0 node1 index
    1 node2 index
    2 k constant

"""

def init_particles(n):
    return np.zeros(n * 9).reshape(n, 9)

def init_anchors(n):
    return np.zeros(n * 2).reshape(n, 2)

def init_springs(n):
    return np.zeros(n * 3).reshape(n, 3)

def hookes(x1, y1, x2, y2, d, k):
    return -k*(((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))**0.5 - d)

def dir_to(x1, y1, x2, y2):
    l = ((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))**0.5
    return np.array([(x1-x2)/l, (y1-y2)/l])

a = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0,],[ 0, 5, 0, 0, 0, 0, 0, 0, 0,]]
b = [[0, 1]]
c = [[0, 6]]
p = np.array(a, np.float64)
si = np.array(b, np.int16)
sd = np.array(c, np.float64)
DT = 0.1
T = 0
DAMP = 10
G = np.array([0, -9.81])


def verlet():
    global p, s, DT, T
    n_pos = p[...,0:2] * 2 - p[...,4:6] + p[...,2:4] * DT * DT
    p[...,4:6], p[...,0:2] = p[...,0:2], n_pos
    p[...,6:8] = (p[...,0:2] - p[...,4:6]) / DT
    T = T + DT

def constrain():
    global p, si, sd
    p[...,2:4] = p[...,2:4] * 0 + G
    for x in sd:
        i = x[0]
        p1i = si[i,
        f1 = hookes(p[x[0],0], p[x[0],1], p[x[1],0], p[x[1],1], x[2])
        f2 = -f1
        d1 = dir_to(p[x[0],0], p[x[0],1], p[x[1],0], p[x[1],1])
        d2 = -d1
        p[x[0],2:4] =  p[x[0],2:4] + d1 * f1 
        p[x[1],2:4] =  p[x[1],2:4] + d1 * f1 

def parr():
    print(p)
    print(s)

parr()
constrain()
parr()

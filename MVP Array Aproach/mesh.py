#mesh.py

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

n_p, n_s = 3, 2



G = np.array([0, -9.81])

G = np.array([0, 0], float)
DT = 0.01
T = 0
K = 10
DAMP = 10

## PARTICLES 
pos = np.zeros((n_p, 2), float)
acc = np.zeros((n_p, 2), float)
acc[...] = G
p_pos = np.zeros((n_p, 2), float)
vel = np.zeros((n_p, 2), float)
mass = np.zeros((n_p, 2), float)

## SPRINGS
spring = np.zeros((n_s, 2), int)
dist = np.zeros(n_s, float)


def get_data():
	print("time: ", T)
	print("pos: \n", pos)
	print("vel: \n", vel)
	print("acc: \n", acc)
	print("–––––––––")
	print("spring: \n", spring)
	print("dist: \n", dist)

pos = np.array([[0,0],[5,5],[10,0]])
p_pos = pos
spring = np.array([[0,1],[1,2]], int)
mass = mass+10

def verlet():
    global pos, p_pos, vel, T
    n_pos = pos * 2 - p_pos + acc * DT * DT
    p_pos, pos = pos, n_pos
    vel = (pos - p_pos) / DT
    T = T + DT

def hookes(x):
	force = (x - dist) * K
	return force

def constrain():
	global acc
	diff = (pos[spring[...,0]] - pos[spring[...,1]])
	# using and einstien summaiton to take the magnitude of vectors
	x = np.sqrt(np.einsum('ij,ij->i',diff, diff))
	di = diff / x
	acc[...] = G 
	acc[spring[...,0]] = acc[spring[...,0]]*0 + di*hookes(x)/mass[spring[...,0]]
	acc[spring[...,1]] = acc[spring[...,0]]*0 - di*hookes(x)/mass[spring[...,0]]


def get_dist():
	diff = (pos[spring[...,0]] - pos[spring[...,1]])
	# using and einstien summaiton to take the magnitude of vectors
	return np.sqrt(np.einsum('ij,ij->i',diff, diff))

def set_dist():
	global dist
	diff = (pos[spring[...,0]] - pos[spring[...,1]])
	# using and einstien summaiton to take the magnitude of vectors
	dist = np.sqrt(np.einsum('ij,ij->i',diff, diff))
	print(dist)






set_dist()
def main():
	for i in range(10000):
		constrain()
		verlet()

main()
# import time
# start_time = time.time()
# main()
# print("--- %s seconds ---" % (time.time() - start_time))



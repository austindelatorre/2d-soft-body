import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


n_p, n_s = 3, 2
## PARTICLES 
pos = np.zeros(n_p*2).reshape(n_p, 2)
acc = np.zeros(n_p*2).reshape(n_p, 2)
p_pos = np.zeros(n_p*2).reshape(n_p, 2)
vel = np.zeros(n_p*2).reshape(n_p, 2)
mass = np.zeros(n_p) + 1

## SPRINGS
springs = np.array(np.zeros(n_s*2).reshape(n_s, 2), int)
d = np.zeros(n_s)
k = np.zeros(n_s)
damp = np.zeros(n_s)


G = np.array([0, -9.81], float)
DT = 1
T = 0

def get_data():
	print("pos: \n", pos)
	print("acc: \n", acc)
	print("springs: \n", springs)

def verlet():
	global pos, p_pos, vel, T
	n_pos = pos * 2 - p_pos + acc * DT * DT
	p_pos, pos = pos, n_pos
	vel = (pos - p_pos) / DT
	T = T + DT

def constraints():
	global acc
	acc = acc * 0 + G
	for i in range(n_s):
		# diff represents the vector difference between p1 and p2
		diff = (pos[springs[i, 0]] - pos[springs[i, 1]])
		# dist_a = the actual distance of diff
		dist_a = np.linalg.norm(diff)
		# f = -k * delta distatance * normalized direction: 2d np.array
		f = -k[i] * (dist_a - d[i]) * (diff) / dist_a
		# apply the force
		acc[springs[i, 0]] +=  f / mass[springs[i, 0]]
		acc[springs[i, 1]] += -f / mass[springs[i, 0]]


pos[...,1] = [0, 5, 10]
springs[...,1] = [1,2]
d[...] = [5, 15]
k[...] = 10

get_data()
# plt.scatter(pos.T[0], pos.T[1])
# plt.show()
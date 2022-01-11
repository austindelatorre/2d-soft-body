# mesh_main.py



import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
def mesh_gen(N):
	nodes = [(i//N, i%N) for i in range(N*N)]
	edges = []
	for i, n in enumerate(nodes):
		x = n[0]
		y = n[1]
		if (x < N - 1) and (y < N - 1):
			edges.append((i,i+1))
			edges.append((i,i+N))
			edges.append((i,i+N+1))
			edges.append((i+N,i+1))
		elif (x < N - 1) and not (y < N - 1):
			edges.append((i,i+N))
		elif not (x < N - 1) and (y < N - 1):
			edges.append((i,i+1))
	return nodes, edges


N = 5
nodes, edges = mesh_gen(N)


n_p, n_s = len(nodes), len(edges)

G = np.array([0, -1])
DT = 0.01
T = 0
K = 2000
DAMP = 10

## PARTICLES 
pos = np.zeros((n_p, 2), float)
acc = np.zeros((n_p, 2), float)
acc[...] = G
p_pos = np.zeros((n_p, 2), float)
vel = np.zeros((n_p, 2), float)
mass = np.zeros((n_p,1), float)
anchor = np.array([])

## SPRINGS
spring = np.zeros((n_s, 2), int)
dist = np.zeros(n_s, float)


def get_data():
	print("########################")
	print("time: ", T)
	print("pos: \n", pos)
	print("vel: \n", vel)
	print("acc: \n", acc)
	print("–")
	print("spring: \n", spring)
	print("dist: \n", dist)

def verlet():
    global pos, p_pos, vel, T
    n_pos = pos * 2 - p_pos + acc * DT * DT
    n_pos[anchor] = p_pos[anchor]
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
	di = (diff.T/x).T
	f = hookes(x)
	f = f.reshape(f.size, 1)
	acc[spring[...,0]] = acc[spring[...,0]]*0 + G - (di*f)/mass[spring[...,0]]
	acc[spring[...,1]] = acc[spring[...,1]]*0 + G + (di*f)/mass[spring[...,1]]
	print(acc)

def get_dist():
	diff = (pos[spring[...,0]] - pos[spring[...,1]])
	# using and einstien summaiton to take the magnitude of vectors
	return np.sqrt(np.einsum('ij,ij->i',diff, diff))

def set_dist():
	global dist
	diff = (pos[spring[...,0]] - pos[spring[...,1]])
	# using and einstien summaiton to take the magnitude of vectors
	dist = np.sqrt(np.einsum('ij,ij->i',diff, diff))

def run():
	verlet()
	constrain()


def get_edge():
	lines = []
	for e in spring:
		lines.append((pos[e[0]], pos[e[1]]))
	return lines


mass = mass + 1
achrs = [(0, N-1), (N-1,N-1)]
anchor = np.array([nodes.index(i) for i in achrs])
pos = p_pos = np.array(nodes)
spring = np.array(edges)

set_dist()

def plot():
	fig = plt.figure(figsize = (4, 4))
	ax = plt.axes(xlim = (-15, 15), ylim = (-15, 15))
	scatter = ax.scatter(pos[..., 0], pos[..., 1], c=acc[..., 1], cmap='Greens')
	line_segments = LineCollection(get_edge(),
	                               linewidths=(0.5),
	                               linestyles='solid')
	# line_segments.set_array(x)
	ax.add_collection(line_segments)

	def update(frame_number):
		scatter.set_offsets(pos)
		scatter.set_array(c=acc[..., 1])
		line_segments.set_segments(get_edge())
		run()
		return scatter, line_segments

	anim = FuncAnimation(fig, update, interval = 10)
	plt.show()


plot()










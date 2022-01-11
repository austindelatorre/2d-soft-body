# mesh_main.py



import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection


n_p, n_s = 2, 1

G = np.array([0, -5])
DT = 0.1
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
anchor = np.array([0])

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
	acc[...] = G 
	acc[spring[...,0]] = acc[spring[...,0]]*0 + G - di*hookes(x)/mass[spring[...,0]]
	acc[spring[...,1]] = acc[spring[...,0]]*0 + G + di*hookes(x)/mass[spring[...,0]]

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


def get_edge():
	x = np.array([pos[spring[...,[0]]], pos[spring[...,[1]]]])
	x = np.ravel(x).reshape(1, spring.size,2)
	return x


def run():
	verlet()
	constrain()



pos = np.array([[0,0],[0,5]])
p_pos = pos
spring = np.array([[0,1]], int)
mass = mass+10
dist[...] = 4
set_dist()

anchor = np.array([1])
get_data()
get_edge()




def plot():
	fig = plt.figure(figsize = (4, 4))
	ax = plt.axes(xlim = (-15, 15), ylim = (-15, 15))
	scatter = ax.scatter(pos[..., 0], pos[..., 1])
	line_segments = LineCollection(get_edge(),
	                               linewidths=(0.5),
	                               linestyles='solid')
	# line_segments.set_array(x)
	ax.add_collection(line_segments)

	def update(frame_number):
		scatter.set_offsets(pos)
		
		line_segments.set_segments(get_edge())
		run()
		return scatter, line_segments

	anim = FuncAnimation(fig, update, interval = 10)
	plt.show()


plot()






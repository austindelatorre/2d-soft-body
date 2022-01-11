

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection


#### TESTING UTILITY ####
def nda(l):
	return np.array(l)

#########################

def mesh_gen(N):
	nodes = [(i//N, i%N) for i in range(N*N)]
	edges = []
	for i, n in enumerate(nodes):
		x = n[0]
		y = n[1]
		if (x < N - 1) and (y < N - 1):
			edges.append((i,i+1))
			edges.append((i,i+N))
			# edges.append((i,i+N+1))
			# edges.append((i+N,i+1))
		elif (x < N - 1) and not (y < N - 1):
			edges.append((i,i+N))
		elif not (x < N - 1) and (y < N - 1):
			edges.append((i,i+1))
	return nodes, edges



edges = [[0,1],[1,2],[2,3],[3,0],[0,2], [1,3], [3,5],[0,4],[4,5],]
nodes = [[0,0],[0,5],[5,5], [5,0],[0,-5],[5,-5]]
state = [True, False, False, True,True,True]

nodes, edges = mesh_gen(3)
achrs = [(0, 2), (2,2)]
state = [True for i in nodes]
print(nodes)
print(edges)
for a in achrs:
	if a in nodes:
		state[nodes.index(a)] = False

n_particles = len(nodes)
n_springs = len(edges)

T = 0
DT = 0.00001
K = 100
G = nda([0, -10])
DAMP= 0.6
M = 1



##########################
particle_dt = [	('pos', np.float64, 2),
			  	('p_pos', np.float64, 2),
				('acc', np.float64, 2),
				('vel', np.float64, 2),
				('mass', np.float64),
				('free', bool)]

spring_dt = [	('nodes', np.uintc, 2),
				('d', np.float64),
				('dir', np.float64, 2)]

particles = np.zeros((n_particles), dtype=particle_dt)
springs = np.zeros((n_springs), dtype=spring_dt)
##########################

def init_dist():
	global springs
	v_diff \
		= particles['pos'][springs['nodes'][:,0]] \
		- particles['pos'][springs['nodes'][:,1]]
	# using and einstien summaiton to take the magnitude of vectors
	distance = np.sqrt(np.einsum('ij,ij->i',v_diff, v_diff))
	springs['d'] = distance
	distance = distance.reshape(distance.size, 1)
	springs['dir'] = -v_diff/distance

def print_data():
	print("**************************************************************")
	print("Data @ T = ", T)
	print("\tSprings: \n", springs)
	print("\tParticles: \n", particles)

particles["pos"] = particles["p_pos"] = nda(nodes)
springs["nodes"] = nda(edges)
particles["mass"] = M
particles["free"] = nda(state)
particles["acc"] = G
init_dist()
print(state)
print_data()
#####################

def verlet_stormer():
	global particles, T
	
	# n_pos = pos * 2 - p_pos + acc * DT**2
	n_pos = particles["pos"][particles["free"]] * 2 \
		- particles["p_pos"][particles["free"]] \
		+ particles["acc"][particles["free"]] * DT * DT
	particles["p_pos"][particles["free"]] = particles["pos"][particles["free"]]

	particles["pos"][particles["free"]] = n_pos

	particles["vel"][particles["free"]] \
		= (particles["pos"][particles["free"]] \
		- particles["p_pos"][particles["free"]]) / DT

def verlet_velocity():
	global particles, T

	particles['acc'] \
		-= 0.5 * DAMP * particles['vel'] * abs(particles['vel'])
	
	n_pos = particles["pos"][particles["free"]] \
		+ particles["vel"][particles["free"]] * DT \
		+ particles["acc"][particles["free"]] * DT * DT * 0.5
	
	particles["p_pos"][particles["free"]] = particles["pos"][particles["free"]]

	particles["pos"][particles["free"]] = n_pos

	particles["vel"][particles["free"]] \
		= particles["vel"][particles["free"]] \
		+ particles["acc"][particles["free"]] * DT


def hooke():
	global particles
	particles['acc'] = G

	v_diff \
		= particles['pos'][springs['nodes'][:,0]] \
		- particles['pos'][springs['nodes'][:,1]]
	# using and einstien summaiton to take the magnitude of vectors
	distance = np.sqrt(np.einsum('ij,ij->i',v_diff, v_diff))
	distance = distance.reshape(distance.size, 1)
	direction = -v_diff/distance
	m_diff = springs['d'] - distance.ravel() 
	force = - m_diff * K

	particles['acc'][springs['nodes'][:,0]] \
		+= direction * (force / particles['mass'][springs['nodes'][:,0]]).reshape(force.size, 1)

	particles['acc'][springs['nodes'][:,1]] \
		-= direction * (force / particles['mass'][springs['nodes'][:,1]]).reshape(force.size, 1) 
	
	

def run():
	global T
	hooke()
	verlet_velocity()
	# verlet_stormer()
	
	# collision
	T = T + DT



def main():
	for _ in range(5):
		run()
	print_data()

def plot():
	def get_edge():
		lines = []
		for e in springs['nodes']:
			lines.append((particles['pos'][e[0]], particles['pos'][e[1]]))
		return lines
	fig = plt.figure(figsize = (4, 4))
	ax = plt.axes(xlim = (-1, 5), ylim = (-1, 5))
	scatter = ax.scatter(particles['pos'][..., 0], particles['pos'][..., 1])
	line_segments = LineCollection(get_edge(), linewidths=(0.5), linestyles='solid')
	ax.add_collection(line_segments)

	def update(frame_number):
		scatter.set_offsets(particles['pos'])
		line_segments.set_segments(get_edge())
		for _ in range(1000):
			run()
		print_data()
		return scatter, line_segments

	anim = FuncAnimation(fig, update, interval = 10)
	plt.show()


plot()













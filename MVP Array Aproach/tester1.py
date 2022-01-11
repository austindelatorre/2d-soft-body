

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
#### TESTING UTILITY ####
def nda(l):
	return np.array(l)

#########################

edges = [[0,1],[1,2],[2,0],]
nodes = [[0,0],[5,5],[10,0]]
state = [True, False, True]
n_particles = len(edges)
n_springs = len(nodes)

T = 0
DT = 0.0002
K = 50
G = nda([0, -10])
DAMP=1
M = 5



##########################
particle_dt = [	('pos', np.float64, 2),
			  	('p_pos', np.float64, 2),
				('acc', np.float64, 2),
				('vel', np.float64, 2),
				('mass', np.float64),
				('free', bool)]

spring_dt = [	('nodes', np.uintc, 2),
				('d', np.float64)]

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
	
	# n_pos = pos * 2 - p_pos + acc * DT**2
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
	
	particles['acc'][springs['nodes'][:,0]] \
		-= particles['vel'][springs['nodes'][:,0]] * DAMP

	particles['acc'][springs['nodes'][:,1]] \
		-= particles['vel'][springs['nodes'][:,1]] * DAMP

def run():
	global T
	hooke()
	# verlet_velocity()
	verlet_stormer()
	
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
	ax = plt.axes(xlim = (-15, 15), ylim = (-15, 15))
	scatter = ax.scatter(particles['pos'][..., 0], particles['pos'][..., 1])
	line_segments = LineCollection(get_edge(), linewidths=(0.5), linestyles='solid')
	ax.add_collection(line_segments)

	def update(frame_number):
		scatter.set_offsets(particles['pos'])
		line_segments.set_segments(get_edge())
		for _ in range(50):
			run()
		return scatter, line_segments

	anim = FuncAnimation(fig, update, interval = 10)
	plt.show()


plot()













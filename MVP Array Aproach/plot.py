import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

DT = 0.005
n = 20
ns = 1

particles = np.zeros(n, dtype = 
[	("pos", float, 2),
	("vel", float, 2),
	("acc", float, 2),
	("p_pos", float, 2),
	("mass", float, 1) ])

springs = np.zeros(ns, dtype = 
[	("edges", int, 2),
	("dist", float, 1) ])

particles["pos"] = np.zeros((n, 2))
particles["vel"] = np.zeros((n, 2))
particles["acc"] = np.zeros((n, 2))
particles["p_pos"] = np.zeros((n, 2))
particles["mass"] = np.zeros(n)

springs["edges"] = np.zeros((n, 2), int)
springs["dist"] = np.zeros(n, float)

def init_data():
	


fig = plt.figure(figsize = (30, 30))
ax = plt.axes(xlim = (0, 30), ylim = (0, 30))
scatter = ax.scatter(particles["position"][: , 0], particles["position"][: , 1])

def update(frame_number):
	scatter.set_offsets(particles["position"])
	progress()
	return scatter

anim = FuncAnimation(fig, update, interval = 10)
plt.show()
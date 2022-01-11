def gen_mesh(N):
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


def testing(N):
	import matplotlib.pyplot as plt
	import numpy as np
	from matplotlib.collections import LineCollection

	
	nodes, edges = gen_mesh(N)
	pos = np.array(nodes)
	lines = []
	for e in edges:
		lines.append((nodes[e[0]], nodes[e[1]]))


	fig = plt.figure(figsize = (4, 4))
	ax = plt.axes(xlim = (-1, N+3), ylim = (-1, N+3))
	scatter = ax.scatter(pos[..., 0], pos[..., 1])
	line_segments = LineCollection(lines, linewidths=(0.5), linestyles='solid')
	ax.add_collection(line_segments)
	plt.show()


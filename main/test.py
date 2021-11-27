import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
from vector import Vector



fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.add_patch(plt.Rectangle((0,0), 10, 10, fc='k', ec='w'))
ax.axis('equal')
ax.axis('off')

for i in range(100):
    ax.add_patch(plt.Rectangle((randint(0,100)/10, randint(0,100)/10), 0.05, 0.05, fc='tab:purple'))

# def init():
#     obj_frames
#     frame_set = list()


#     for frame in obj_frame:
#         for dot in frame.dots:

#     return frame_set


# def animate(i):
#     for dot in frame_set[i].dots:
#         dot.set_center((X, Y))

#     for line in frame_set[i].dots:
#         line.set_center((X, Y))
#     pass


plt.show()
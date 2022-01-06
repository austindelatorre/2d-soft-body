import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
from vector import Vector


class Dot:
    pos = Vector(0,0)

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Frame:
    lines = list()
    dots = list()

    def add_dot(self, dot):
        self.dots.append(dot)

    def add_line(self, line):
        self.lines.append(line)

class Scene:
    frames = list()
    def add_frame(self, frame):
        self.frames.append(frame)

    def render_scene(self, t=10, dt=0.1):
        obj_frames = self.frames

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

sc = Scene()
sc.render_scene()



















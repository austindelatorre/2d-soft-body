

# This program can take very simple point particls with initial
# vel, acc, pos and simulate constant acc physics acting on them.
# It produces a very simple plot of every moment in the simulation.
### globals ###
CONSTANT_ACC_X = 0.0
CONSTANT_ACC_Y = -9.8



class Vector:
    x = 0.0
    y = 0.0

    # constructor
    def __init__(self, x = 0.0, y = 0):
        self.x = float(x)
        self.x = float(x)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    length = magnitude = __abs__

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Vector("+str(self.x)+", "+str(self.y)+")"



class Particle:
    pos = Vector(0.0, 0.0)
    vel = Vector(0.0, 0.0)
    acc = Vector(0.0, 9.8)
    mass = 1.0

    def __init__(self, pos = Vector(0,0), vel = Vector(0,0), acc = Vector(CONSTANT_ACC_Y,CONSTANT_ACC_X), mass = 1.0):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def update(self, dt):
        pos_new = self.pos + self.vel*dt + self.acc*(dt*dt*0.5)
        acc_new = self.acc # can add functionality for dynamic forces/drag here
        vel_new = self.vel + (self.acc + acc_new)*(dt*0.5)
        self.pos = pos_new
        self.vel = vel_new
        self.acc = acc_new

    def __str__(self):
        return "Particle("+str(self.pos)+", "+str(self.vel)+")"

class World:
    dt = 1
    t = 10
    particles = list()
    plot = list()

    def __init__(self, particles):
        self.particles = particles

    def run(self):
        for moment in range(int(self.t/self.dt)):
            for particle in self.particles:
                print(self.dt)
                particle.update(self.dt)
                print(particle)
            self.plot.append(self.particles)
        print(self.plot)

world = World([Particle()])
world.run()




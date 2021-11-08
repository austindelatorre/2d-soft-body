
### GLOBAL CONSTANTS ###
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

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def normalized(self):
        l = self.magnitude()
        if l:
            return Vector(self.x / l, self.y / l)

    def __str__(self):
        return "Vector(X: "+str(self.x)+", Y: "+str(self.y)+")"


class Particle:
    pos = Vector(0.0, 0.0)
    vel = Vector(0.0, 0.0)
    acc = Vector(0.0, 9.8)
    mass = 1.0

    def __init__(self, pos = Vector(0,0), vel = Vector(0,0), acc = Vector(CONSTANT_ACC_Y, CONSTANT_ACC_X), mass = 1.0):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def ApplyForce(self, force):
        if self.Particle.mass != 0.0:
            self.acc += force / self.material.mass

    def update(self, dt):
        pos_new = self.pos + self.vel*dt + self.acc*(dt*dt*0.5)
        acc_new = self.acc # can add functionality for dynamic forces/drag here
        vel_new = self.vel + (self.acc + acc_new)*(dt*0.5)
        self.pos = pos_new
        self.vel = vel_new
        self.acc = acc_new



    def __str__(self):
        return "Particle("+str(self.pos)+", "+str(self.vel)+")"

class Constraint:

    node1  = None   # first constrained particle
    node2  = None   # second constrained particle
    target = 0.0    # target distance the particles try to maintain from one another
    stiff  = 1.0    # Hooke's law spring constant [0.0, 1.0] (0 = no spring, 1 = rigid bar)
    damp   = 0.0    # Hooke's law dampening constant

    def __init__(self, p1, p2, s, d=None):
        self.node1  = p1
        self.node2  = p2
        self.stiff  = s
        if d == None:
            self.target = ((p2.position.x - p1.position.x)**2 + (p2.position.y - p1.position.y)**2)**0.5
        else:
            self.target = d


    # Attempt to maintain the target distance between the two constrained particles. Calculate the
    # distance between the two particles and apply a restoring impulse to each particle.

    def Relax(self):
        D = abs(self.node2.pos - self.node1.pos)
        F = 0.5 * self.stiff * (D.length() - self.target) * D.normalized()
        if self.node1.material.mass != 0.0 and not self.node2.material.mass:
            self.node1.ApplyImpulse(2.0 * +F)
        elif not self.node1.material.mass and self.node2.material.mass != 0.0:
            self.node2.ApplyImpulse(2.0 * -F)
        else:
            self.node1.ApplyImpulse(+F)
            self.node2.ApplyImpulse(-F)

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


def main():
    world = World([Particle()])
    world.run()

main()




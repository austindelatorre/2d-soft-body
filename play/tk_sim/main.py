### PHYSICS ###



class Particle:

    def __init__(self, pos, vel = Vector(), acc = Vector()):
        self.pos = pos
        self.pos_last = pos
        self.vel = vel
        self.acc = acc

    def distance_to(self, other):
        return self.pos.distance_to(other.pos)

    def update(self):
        self.vel = (self.pos - self.pos_past)
        self.pos_past = self.pos
        self.pos = self.pos + vel_n
        self.pos = self.pos + Vector(0, 9.8)

class Constraint:

    def __init__(self, p1, p2, k, l=None):
        self.p1 = p1
        self.p2 = p2
        self.k = k
        if l == None:
            p1.distance_to(p1)
        else:
            self.l = l

    def update(self):
        pass

class Mesh:
    def __init__(self):
        self.particles = list()
        self.constraints = list()

    def add_particle(self, particle):
        self.particles.append(particle)

    def add_constraint(self, constraint):
        self.constraint.append(constraint)

    def update(self):
        pass

    def render(self):
        pass

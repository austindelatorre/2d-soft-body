# Vector.py
# Custom two-dimentional vector class for easy creation and manipulation of vectors. Contains
# standard arithmetic operations between vectors and coefficients (addition, subtraction, and
# multiplication), as well as a number of handy operations that are commonly used (dot product,
# normalization, etc.)


import math
import operator
import pygame as game


class Vector:
    x = 0.0
    y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    length = magnitude = __abs__

    def normalize(self):
        l = self.magnitude()
        if l:
            self.x = self.x / l
            self.y = self.y / l

    def normalized(self):
        l = self.magnitude()
        if l:
            return Vector(self.x / l, self.y / l)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def one(self):
        self.x = 1.0
        self.y = 1.0

    def tuple(self):
        return (self.x, self.y)

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0.0 or self.y != 0.0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __iadd_(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        assert type(other) in (int, float)
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        assert type(other) in (int, float)
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        assert type(other) in (int, float)
        self.x *= other
        self.y *= other
        return self

    def __div__(self, other):
        assert type(other) in (int, float)
        return Vector(operator.div(self.x, other),
                      operator.div(self.y, other))

    def __idiv__(self, other):
        assert type(other) in (int, float)
        operator.div(self.x, other)
        operator.div(self.y, other)
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __pos__(self):
        return Vector(self.x, self.y)

    def __str__(self):
        return "Vector("+str(self.x)+", "+str(self.y)+")"

    @staticmethod
    def zero():
        return Vector(0.0, 0.0)

class Material:
    friction = 0.4  # coefficient of friction [0.0, 1.0] (0 = ice, 1 = glue)
    bounce   = 0.4  # coefficient of resitution [0.0, 1.0] (0 = inelastic, 1 = elastic)
    mass     = 1.0  # physical mass

    # Class constructor. Define the material's/particle's properties.
    # @param    f   coefficient of friction [0.0, 1.0]
    # @param    b   coefficient of restitution [0.0, 1.0]
    # @param    m   mass
    # @return   null

    def __init__(self, f=0.4, b=0.4, m=1.0, d=0.01):
        if f >= 0.0 and f <= 1.0:
            self.friction = f
        if b >= 0.0 and b <= 1.0:
            self.bounce = b
        if m >= 0.0:
            self.mass = m

class Particle:
    #
    material     = None              # particle material
    world        = None              # world particle is simulated in
    position     = Vector(0.0, 0.0)  # current position
    previous     = Vector(0.0, 0.0)  # previous time-step [t-dt] position
    velocity     = Vector(0.0, 0.0)  # [readme] particle velocity
    acceleration = Vector(0.0, 0.0)  # acceleration of the particle


    # Class constructor. Initialize the particle within the simulation world.
    #
    # @param    world       reference to the simulation world this particle resides in
    # @param    x           particle horizontal position relative to the world
    # @param    y           particle vertical position relative to the world
    # @param    material    specify this particle's material; default if none provided
    # @return   null
    #
    def __init__(self, world, x=0.0, y=0.0, material=None):
        self.world    = world
        self.position = Vector(x, y)
        self.previous = Vector(x, y)
        if material == None:
            self.material = Material()
        else:
            self.material = material


    # Simulate this particle's motion. A mass of zero denotes that the particle is 'pinned', and
    # cannot move.
    #
    # @param    null
    # @param    null
    #
    def Simulate(self):
        if not self.material.mass:
            return
        self.velocity = 2.0 * self.position - self.previous
        self.previous = self.position
        self.position = self.velocity + self.acceleration * self.world.delta**2.0
        self.velocity = self.position - self.previous
        self.acceleration = Vector.zero()


    # Accelerate this particle. This method affects the particle's acceleration, disregarding mass.
    # Use this if you need to immediately affect the particle's acceleration.
    #
    # @param    rate    applied acceleration (m/s^2)
    # @return   null
    #
    def Accelerate(self, rate):
        self.acceleration += rate


    # Apply a force to this particle. This method affect's the particle's acceleration, taking it's
    # mass into account. To move an object, a large enough force must be applied to immediately
    # move it, or a smaller force over time must be applied.
    #
    # @param    force   force applied to the particle (N)
    # @return   null
    #
    def ApplyForce(self, force):
        if self.material.mass != 0.0:
            self.acceleration += force / self.material.mass


    # Apply an impulse to this particle. This method affect's the particle's velocity, taking it's
    # mass into account. Since the particle is simulated via Verlet integration, a change in the
    # particle's position results in an immediate change in velocity. Use this method to
    # immediately affect the particle's velocity.
    #
    # @param    impulse     impulse directly applied to the particle (a*dt / m)
    def ApplyImpulse(self, impulse):
        if self.material.mass != 0.0:
            self.position += impulse / self.material.mass


    # Set the acceleration of this particle to zero. By applying forces and resetting them after,
    # we ensure that the forces must be applied every time step of the simulation in order to be
    # regarded as a continuous force.
    #
    # @param    null
    # @return   null
    #
    def ResetForces(self):
        self.acceleration = Vector.zero()


    # Restrain this particle to the simulation world boundaries. If a particle exceeds the world
    # boundaries, we bounce it back into the world. We do this by correcting the particle's current
    # position to the boundary line, and adjust the previous position so that next time step the
    # particle maintains a velocity that is accurate as such the particle takes into account
    # restitution and friction.
    #
    # @param    null
    # @return   null
    #
    def Restrain(self):
        # screen boundries
        if self.position.x < 0.0:
            distance = self.position - self.previous
            self.position.x = -self.position.x
            self.previous.x = self.position.x + self.material.bounce * distance.y
            #
            j = distance.y
            k = distance.x * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.y -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.y -= k

        elif self.position.x > self.world.size.x:
            distance = self.position - self.previous
            self.position.x = 2.0 * self.world.size.x - self.position.x
            self.previous.x = self.position.x + self.material.bounce * distance.y
            #
            j = distance.y
            k = distance.x * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.y -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.y -= k

        if self.position.y < 0.0:
            distance = self.position - self.previous
            self.position.y = -self.position.y
            self.previous.y = self.position.y + self.material.bounce * distance.y
            #
            j = distance.x
            k = distance.y * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.x -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.x -= k

        elif self.position.y > self.world.size.y:
            distance = self.position - self.previous
            self.position.y = 2.0 * self.world.size.y - self.position.y
            self.previous.y = self.position.y + self.material.bounce * distance.y
            #
            j = distance.x
            k = distance.y * self.material.friction
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.position.x -= 2.0 * j
            else:
                if k * t > 0.0:
                    self.position.x -= k

class Constraint:
    #
    node1  = None   # first constrained particle
    node2  = None   # second constrained particle
    target = 0.0    # target distance the particles try to maintain from one another
    stiff  = 1.0    # Hooke's law spring constant [0.0, 1.0] (0 = no spring, 1 = rigid bar)
    damp   = 0.0    # Hooke's law dampening constant


    # Class constructor. Grab references of the two constrained particles, get a specified spring
    # constant for the constraint, and establish a target distance between the particles.
    #
    # @param    p1  first particle constrained
    # @param    p2  second particle constrained
    # @param    s   spring constant [0.0, 1.0]
    # @param    d   distance constraint (default seprerating distance)
    # @return   null
    #
    def __init__(self, p1, p2, s, d=None):
        #
        self.node1  = p1
        self.node2  = p2
        self.stiff  = s
        if d is None:
            self.target = math.sqrt((p2.position.x - p1.position.x)**2 + (p2.position.y - p1.position.y)**2)
        else:
            self.target = d


    # Attempt to maintain the target distance between the two constrained particles. Calculate the
    # distance between the two particles and apply a restoring impulse to each particle.
    #
    # @param    null
    # @return   null
    #
    def Relax(self):
        #
        D = self.node2.position - self.node1.position
        F = 0.5 * self.stiff * (D.length() - self.target) * D.normalized()
        if self.node1.material.mass != 0.0 and not self.node2.material.mass:
            self.node1.ApplyImpulse(2.0 * +F)
        elif not self.node1.material.mass and self.node2.material.mass != 0.0:
            self.node2.ApplyImpulse(2.0 * -F)
        else:
            self.node1.ApplyImpulse(+F)
            self.node2.ApplyImpulse(-F)
            
class Composite:
    #
    particles   = list()    # list of particles composing this shape
    constraints = list()    # list of constraints composing this shape


    # Class constructor. Add passed particles and constraints to composite lists.
    #
    # @param    *params     tuple of Particle and Constraint objects defining this shape
    # @return   null
    #
    def __init__(self, *params):
        for param in self.traverse(params):
            if isinstance(param, Particle):
                self.particles.append(param)
            elif isinstance(param, Constraint):
                self.constraints.append(param)
            print (len(self.particles))


    # Add an arbitrary number of particles to this shape.
    #
    # @param    *particles  tuple of Particle objects
    # @return   null
    #
    def AddParticles(self, *particles):
        for particle in particles:
            if isinstance(particle, Particle):
                self.particles.append(particle)


    # Add an arbitrary number of constraints to this shape.
    #
    # @param    *constraints    tuple of Constraint objects
    # @return   null
    #
    def AddConstraints(self, *constraints):
        for constraint in constraints:
            if isinstance(constraint, Constraint):
                self.constraints.append(constraint)


    # Set a global material to all particles in this shape.
    #
    # @param    material    material to be applied to all particles
    # @return   null
    #
    def SetMaterial(self, material):
        for particle in self.particles:
            particle.material = material


    # Traverses and nested tuples and yields only the values inside. Used for parsing class
    # constructor arguements; it is beneficial to pass two tuples, one of particles and the other
    # of constraints, so that the particles get added to the composite first, allowing the
    # constraints to immediately reference them in the constructor.
    #
    # @param    o       tuple of objects and/or tuples
    # @yield    Object  instance found within the passed tuple
    #
    def traverse(self, o):
        if isinstance(o, (list, tuple)):
            for value in o:
                for subvalue in self.traverse(value):
                    yield subvalue
        else:
            yield o

class World:
    size        = Vector(0.0, 0.0)  # world size/boundaries
    hsize       = Vector(0.0, 0.0)  # half-size world size/boundaries
    gravity     = Vector(0.0, 0.0)  # global gravitational acceleration
    step        = 0                 # time step
    delta       = 0.0               # delta time (1.0 / time step)
    #
    particles   = list()            # list of all particles being simulated
    constraints = list()            # list of all constraints being simulated
    composites  = list()            # list of all composite shapes being simulated


    # Class constructor. Initialize the simulation world. Set global constants.
    #
    # @param    s   simulation world size
    # @param    g   global acceleration constant
    # @param    t   number of time steps to simulate per simlation step
    #
    def __init__(self, s=Vector(0.0, 0.0), g=Vector(0.0, 9.8), t=8):
        self.size      = s
        self.hsize     = 0.5 * s
        self.gravity   = g
        if t < 1:
            self.step  = 1
            self.delta = 1.0
        else:
            self.step  = t
            self.delta = 1.0 / self.step


    # Simulate a number of time steps on our simulation world. For each time step, we satisfy
    # constraints between particles, accelerate all particles by the universal gravitational
    # acceleration, simulate motion of each particle, then constraint the particles to the
    # simulation world boundaries.
    #
    # @param    null
    # @return   null
    #
    def Simulate(self):
        for i in range(self.step):
            for particle in self.particles:
                particle.Accelerate(self.gravity)
                particle.Simulate()
                particle.Restrain()
                particle.ResetForces()
            for constraint in self.constraints:
                constraint.Relax()



    # Create and add a particle to the simulation world.
    #
    # @param    x           horizontal position of the particle
    # @param    y           vertical position of the particle
    # @return   Particle    object reference of the new particle
    #
    def AddParticle(self, x, y, mat=None):
        particle = Particle(self, x, y, mat)
        self.particles.append(particle)
        return particle


    # Create and add a constraint between two particles in the simulation world.
    #
    # @param    p1          first particle to be constrained
    # @param    p2          second particle to be constrained
    # @param    s           constraint spring stiffness [0.0, 1.0]
    # @param    d           distance constraint (default seperating distance)
    # @return   Constraint  object reference of the new constraint
    #
    def AddConstraint(self, p1, p2, s, d=None):
        constraint = Constraint(p1, p2, s, d)
        self.constraints.append(constraint)
        return constraint


    # Create and add a composite shape to the simulation world.
    #
    # @param    *params     multiple parameters of Particles and Constraints that make up the shape
    # @return   Composite   object reference of the new composite
    #
    def AddComposite(self, *params):
        composite = Composite(params)
        self.composites.append(composite)
        return composite

class App:
    #
    running   = True                            # keep the application running
    screen    = None                            # window handler pointer
    title     = "Application"                   # application window title
    size      = (0, 0)                          # application window size
    center    = (0, 0)                          # application window position
    flags     = game.HWSURFACE | game.DOUBLEBUF # hardware acceleration and double buffering
    framerate = 30                              # application frame rate


    # Class constructor. Initialize the Pygame window with a title, position, and frame rate.
    #
    # @param    t   application title
    # @param    x   window x-position
    # @param    y   window y-position
    # @param    f   application frame rate
    # @return   null
    #
    def __init__(self, t="Application", x=550, y=400, f=30):
        self.title     = t
        self.size      = (x, y)
        self.center    = (x/2, y/2)
        self.framerate = f
        self.Initialize()


    # Run the application. Manages core functionality of the application, such as updating the
    # window every frame and refreshing the screen, user input through keyboard and mouse, renders
    # content onto the screen, and cleans up the window process once it is time to exit.
    #
    # @param    null
    # @return   null
    #
    def Run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen  = game.display.set_mode(self.size, self.flags)
        self.running = True
        #
        while self.running:
            for event in game.event.get():
                self.HandleEvent(event)
            self.Update()
            self.Render()
            game.time.delay(1000 / self.framerate)
        self.CleanUp()


    # Handles keyboard and mouse events inputted by the end-user.
    #
    # @param    event   Event Object with information on the particular event
    # @return   null
    #
    def HandleEvent(self, event):
        if event.type == game.QUIT:
            self.running = False


    # Clears memory after the application has exited.
    #
    # @param    null
    # @return   null
    #
    def CleanUp(self):
        game.quit()


    # Exit the application.
    #
    # @param    null
    # @return   null
    #
    def Exit(self):
        self.running = False


    # User-defined function that is called a single time after the application has started, but
    # before the main game update loop. Used to define variables and objects before they are called
    # upon every game loop.
    #
    # @param    null
    # @return   null
    #
    def Initialize(self):
        pass


    # User-defined function that is called once per frame. Core game loop that the user can use to
    # update content within their own applicaitons.
    #
    # @param    null
    # @return   null
    #
    def Update(self):
        pass


    # User-defined function that is called once per frame, after the game update function. Used to
    # draw user-created content onto the screen every game loop.
    def Render(self):
        pass

class DemoBlob(App):
    #
    world    = World(Vector(630.0, 470.0), Vector(0, 2), 6)
    blob     = world.AddComposite()
    blobsize = 100
    skinsize = 30
    #
    grabbed  = None
    radius   = 20
    strength = 0.10

    #
    def Initialize(self):
        #
        j = 0.1
        k = 0.9
        steps = 15

        mat = Material(1.0, 0.0, 1.0)

        outer = []
        inner = []
        kinex = []

        # outer skin
        offset = (2.0 * math.pi) / (2 * steps)
        for i in range(steps):
            x = self.world.hsize.x + self.blobsize * math.cos(i * (2.0 * math.pi) / steps + offset)
            y = self.world.hsize.y + self.blobsize * math.sin(i * (2.0 * math.pi) / steps + offset)
            outer.append(self.world.AddParticle(x, y, mat))

        # inner skin
        for i in range(steps):
            x = self.world.hsize.x + (self.blobsize - self.skinsize) * math.cos(i * (2.0 * math.pi) / steps)
            y = self.world.hsize.y + (self.blobsize - self.skinsize) * math.sin(i * (2.0 * math.pi) / steps)
            inner.append(self.world.AddParticle(x, y, mat))

        # connect outer skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], outer[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], outer[0], k))

        # connect inner skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(inner[i-1], inner[i], k))
        kinex.append(self.world.AddConstraint(inner[len(inner)-1], inner[0], k))

        # connect outer-inner skins
        for i in range(steps):
            kinex.append(self.world.AddConstraint(outer[i], inner[i], k))
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], inner[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], inner[0], k))
        """for i in range(1, steps):
            kinex.append(self.world.AddConstraint(inner[i-1], outer[i], k))
        kinex.append(self.world.AddConstraint(inner[len(outer)-1], outer[0], k))"""

        # connect inner skins to anchor point
        self.blob.AddParticles(self.world.AddParticle(self.world.hsize.x, self.world.hsize.y, mat))
        for i in range(steps):
            kinex.append(self.world.AddConstraint(self.blob.particles[0], inner[i], j))

        self.blob.AddParticles(outer, inner)
        self.blob.AddConstraints(kinex)

    #
    def Update(self):
        #
        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
                force = (mouse - self.grabbed.position) * self.strength
                self.grabbed.ApplyImpulse(force)
        else:
            self.grabbed = None
        #
        if game.key.get_pressed()[game.K_ESCAPE]:
            self.Exit()
        self.world.Simulate()


    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (255, 255, 255), pos1, pos2, 1)
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, 2, 0)
        game.display.update()


    #
    def ClosestPoint(self):
        mouse    = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        closest  = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest  = particle
                distance = d
        return (closest, distance)


if __name__ == "__main__":
    print ("Starting...")
    app = DemoBlob("Loco Roco", 640, 480, 30)
    app.Run()
    print ("Ending...")



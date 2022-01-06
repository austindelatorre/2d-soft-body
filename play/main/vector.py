
class Vector:
    x = 0.0
    y = 0.0

    # constructor
    def __init__(self, x = 0.0, y = 0.0):
        self.x = float(x)
        self.x = float(x)
    # pythagorean magnitude/length
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
    length = magnitude = __abs__
    # vector multiplication
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
    # vector addition
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    # vector subtraction
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    # normalizes to unit circle
    def normalized(self):
        l = self.magnitude()
        if l:
            return Vector(self.x / l, self.y / l)
    # provides print format
    def __str__(self):
        return "Vector(X: "+str(self.x)+", Y: "+str(self.y)+")"

    @staticmethod
    def zero():
        return Vector(0.0, 0.0)
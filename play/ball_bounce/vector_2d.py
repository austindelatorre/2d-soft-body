import numpy as np

class Vector:
    """
    Notes:
    
    """

    def __init__(self, *args):
        if len(args) == 0:
            self.xy = np.zeros(2) 
        elif type(args[0]) == np.ndarray:
            self.xy = args[0]
        else:
            self.xy = np.array([args[0], args[1]])

    def __abs__(self):
        return ((self.xy[0]**2 + self.xy[1]**2)**0.5)

    length = magnitude = __abs__

    def __mul__(self, other):
        return Vector(self.xy * np.array(other))

    # vector addition
    def __add__(self, other):
        return Vector(self.xy + np.array(other))

    # vector subtraction
    def __sub__(self, other):
        return Vector(self.xy - np.array(other))

    # normalizes to unit circle
    def normalize(self):
        l = self.magnitude()
        self.xy = Vector().set_arr(self.xy / l)

    # returns normalized to unit circle
    def normalized(self):
        l = self.magnitude()
        return Vector(self.xy / l)

    def distance_to(self, other):
        return (self - other).length()

    # Array Casting
    def __array__(self, dtype=None):
        return self.xy

    def __repr__(self):
        return f"{self.__class__.__name__}(x: {self.xy[0]}, y: {self.xy[1]})"


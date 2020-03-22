
from random import *
from math import *


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = 0
        self.y = 0
        if isinstance(x, tuple) or isinstance(x, list):
            y = x[1]
            x = x[0]
        elif isinstance(x, Vector2D):
            y = x.y
            x = x.x

        self.set(x, y)

    @staticmethod
    def random(size=1):
        sizex = size
        sizey = size
        if isinstance(size, tuple) or isinstance(size, list):
            sizex = size[0]
            sizey = size[1]
        elif isinstance(size, Vector2D):
            sizex = size.x
            sizey = size.y
        return Vector2D(random() * sizex, random() * sizey)

    @staticmethod
    def randomUnitCircle():
        d = random() * pi
        return Vector2D(cos(d) * choice([1, -1]), sin(d) * choice([1, -1]))

    @staticmethod
    def distance(a, b):
        return (a - b).getLength()

    @staticmethod
    def angle(v1, v2):
        return acos(v1.dotproduct(v2) / (v1.getLength() * v2.getLength()))

    @staticmethod
    def angleDeg(v1, v2):
        return Vector2D.angle(v1, v2) * 180.0 / pi

    def set(self, x, y):
        self.x = x
        self.y = y

    def toArr(self):
        return [self.x, self.y]

    def toInt(self):
        return Vector2D(int(self.x), int(self.y))

    def toIntArr(self):
        return self.toInt().toArr()

    def getNormalized(self):
        if self.getLength() != 0:
            f = Vector2D(self)
            self.x = self.x / f.getLength()
            self.y = self.y / f.getLength()
            return self
        else:
            return Vector2D(0, 0)

    def dotproduct(self, other):
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, tuple) or isinstance(other, list):
            return self.x * other[0] + self.y * other[1]
        else:
            return NotImplemented

    def add(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x + other, self.y + other)
        else:
            return NotImplemented

    def sub(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        if isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x - other, self.y - other)
        else:
            return NotImplemented

    def distance(self, b):
        return sqrt((self.x - b.x)**2 + (self.y - b.y)**2)

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        if isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(other.x - self.x, other.y - self.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(other[0] - self.x, other[1] - self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(other - self.x, other - self.y)
        else:
            return NotImplemented

    def scale(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __div__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x / other[0], self.y / other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(other.x / self.x, other.y / self.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(other[0] / self.x, other[1] / self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(other / self.x, other / self.y)
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x**other, self.y**other)
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
            return self
        else:
            return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x -= other[0]
            self.y -= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
            return self
        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x *= other[0]
            self.y *= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            return self
        else:
            return NotImplemented

    def __idiv__(self, other):
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x /= other[0]
            self.y /= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            return self
        else:
            return NotImplemented

    def __ipow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x **= other
            self.y **= other
            return self
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector2D):
            return self.x != other.x or self.y != other.y
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vector2D):
            return self.getLength() > other.getLength()
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Vector2D):
            return self.getLength() >= other.getLength()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Vector2D):
            return self.getLength() < other.getLength()
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Vector2D):
            return self.getLength() <= other.getLength()
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __len__(self):
        return int(sqrt(self.x**2 + self.y**2))

    def getLength(self):
        return sqrt(self.x**2 + self.y**2)

    def lengthSquared(self):
        return sqrt(self.x ** 2 + self.y ** 2)*sqrt(self.x ** 2 + self.y ** 2)
    def toString(self):
        return "["+str(self.x)+","+str(self.y)+"]"

    def __getitem__(self, key):
        if key == "x" or key == "X" or key == 0 or key == "0":
            return self.x
        elif key == "y" or key == "Y" or key == 1 or key == "1":
            return self.y

    def __str__(self):
        return "[x: %(x)f, y: %(y)f]" % self

    def __repr__(self):
        return "{'x': %(x)f, 'y': %(y)f}" % self

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

from helper.BoundingBox.aabb import AABB
from helper.vector2D import Vector2D


class Object:
    def __init__(self):
        self.type = "Object"

class Marchandise(Object):
    def __init__(self, pickup,n):
        EnvironmentalObject.__init__(self)
        self.pickupStation = pickup
        self.mass = 1
        self.volume = 1
        self.type = "Marchandise"
        self.nom=n

class EnvironmentalObject(Object):
    def __init__(self):
        Object.__init__(self)
        self.location = Vector2D(30, 30)
        self.orientation = 0
        self.type = "EnvironmentalObject"


class TargetObjet(EnvironmentalObject):
    def __init__(self, x, y):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.type = "Attractor"


class Wall(EnvironmentalObject):
    def __init__(self, x, y,h,w):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Wall"
        self.aabb = AABB(Vector2D(x,y), h,w)

class Dropoff(EnvironmentalObject):
    def __init__(self, x, y,h,w,id):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D((int(x), int(y)))
        self.id = id
        self.type = "Dropoff"
        self.stock = []
        self.aabb = AABB(Vector2D(x,y), h,w)

class Pickup(EnvironmentalObject):
    def __init__(self, x, y,h,w,id):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = id
        self.type = "Pickup"
        self.stock = []
        self.aabb = AABB(Vector2D(x,y), h,w)
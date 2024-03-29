from helper.BoundingBox.aabb import AABB
from helper.vector2D import Vector2D


class Object:
    def __init__(self):
        self.type = "Object"
        self.nom = "Unknow"

    def __str__(self):
        return 'Type :'+self.type+" nom :"+self.nom

class Marchandise(Object):
    def __init__(self, pickup, n):
        EnvironmentalObject.__init__(self)
        self.pickupStation = pickup
        self.mass = 1
        self.volume = 1
        self.type = "Marchandise"
        self.nom = n


class EnvironmentalObject(Object):
    def __init__(self):
        Object.__init__(self)
        self.location = Vector2D(0, 0)
        self.orientation = 0
        self.type = "EnvironmentalObject"


class TargetObjet(EnvironmentalObject):
    def __init__(self, x=0, y=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.type = "Attractor"


class Wall(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=0, w=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Wall"
        self.aabb = AABB(Vector2D(x, y), h, w)


class Dropoff(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=0, w=0, id=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D((int(x+w/2), int(y+h/2)))
        self.id = id
        self.type = "Dropoff"
        self.stock = []
        self.aabb = AABB(Vector2D(x, y), h, w)


class Pickup(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=0, w=0, id=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = id
        self.type = "Pickup"
        self.stock = []
        self.aabb = AABB(Vector2D(x, y), h, w)


class PerceivedObject(EnvironmentalObject):
    def __init__(self, location = None,aabb = None, type=None):
        self.type = type
        self.location = location
        self.aabb=aabb


class Building(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Building"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "building.png"


class Crossroad(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Crossroad"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "crossroad.png"


class Grass(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Grass"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "grass.png"



class HalfRoad(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "HalfRoad"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "half-road.png"



class House(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "House"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "house.png"



class Road(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Road"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "road.png"



class Turn(EnvironmentalObject):
    def __init__(self, x=0, y=0, h=200, w=200, r=0):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.id = 0
        self.type = "Turn"
        self.aabb = AABB(Vector2D(x, y), h, w)
        self.texture = "turn.png"

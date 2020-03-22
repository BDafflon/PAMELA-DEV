from helper.vector2D import Vector2D


class Object:
    def __init__(self):
        self.type = "Object"


class EnvironmentalObject(Object):
    def __init__(self):
        Object.__init__(self)
        self.location = Vector2D(30, 30)
        self.orientation = 0
        self.type = "EnvironmentalObject"


class Destination(EnvironmentalObject):
    def __init__(self, x, y):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.orientation = 0
        self.type = "Destination"


class TargetObjet(EnvironmentalObject):
    def __init__(self, x, y):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.type = "Attractor"

class Marchandise(EnvironmentalObject):
    def __init__(self, x, y):
        EnvironmentalObject.__init__(self)
        self.location = Vector2D(x, y)
        self.orientation = 0
        self.type = "Marchandise"
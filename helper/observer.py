from helper.vector2D import Vector2D


class Observer:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.dernierePosition = Vector2D(0, 0)
        self.distance=0
        self.distanceTheorique = 0.0
        self.timeout=0

    def update(self, location,type):
        self.distance = self.distance + abs(self.dernierePosition.distance(location))
        self.dernierePosition = Vector2D(location)



class RobotObserver(Observer):
    def __init__(self, id, h):
        Observer.__init__(self, id, "Agent")
        self.idDeplacement = ""
        self.HDepart = h
        self.distance = 0.0
        self.temps = h
        self.nbColis = 0



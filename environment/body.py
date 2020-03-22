from helper import util
from helper.vector2D import Vector2D
from environment.fustrum import CircularFustrum


_BOID_COLLISION_DISTANCE = 45.0
_OBSTACLE_COLLISION_DISTANCE = 250.0
_MAX_COLLISION_VELOCITY = 1.0


class Body:
    def __init__(self):
        self.id = util.id_generator(10, "1234567890")
        self.mass = 1
        self.location = Vector2D(util.randomInt(400), util.randomInt(400))
        self.velocity = Vector2D(util.randomInt(50), util.randomInt(50))
        self.fustrum = CircularFustrum(20)
        self.orientation = 0
        self.vitesseMax = 15
        self.vitesseMin = 1.0
        self.accelerationMax = 15


    def insidePerception(self, p, t):
        return self.fustrum.inside(self.location, p)

    def computeMove(self, v):

        m = Vector2D(v.x, v.y)

        if m.getLength() <= 0:
            m = Vector2D(0, 0)
            return m

        if m.getLength() > self.vitesseMax:
            m = m.getNormalized()
            m = m.scale(self.vitesseMax)

        return m

    def move(self, v):

        self.location.x = self.location.x + v.x
        self.location.y = self.location.y + v.y
        self.velocity = v

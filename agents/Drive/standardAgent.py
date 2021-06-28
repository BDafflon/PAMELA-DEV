import random

from agents.agent import *
from agents.Drive.carAgent import CarAgent
from environment.animateAction import AnimateAction
from environment.application.Drive.agentType import AgentType
from environment.application.Drive.stardardAgentBody import StadardAgentBody
from helper import util
from helper.vector2D import Vector2D


class StandardAgent(Agent):

    def __init__(self, f=1):
        Agent.__init__(self)
        self.body = StadardAgentBody()
        self.type = AgentType.STANDARD
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 10
        self.body.vitesseMax = 50.0
        self.body.vitesseMin = 1.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(random.randint(0,1000), random.randint(0,1000))
        self.obstacleFactor = 0
        self.attractorFactor = 0
        self.name='t'

    def getEditable(self):
        return Agent.getEditable().append(["famille","avoidanceFactor",'obstacleFactor','type'])


    def filtrePerception(self):
        walls = []
        other = []
        dropoff = []
        pickup = []

        for o in self.body.fustrum.perceptionList:
            if o.type == "Wall":
                walls.append(o)
            else:
                if o.type == "Dropoff":
                    dropoff.append(o)
                else:
                    if o.type == "Pickup":
                        pickup.append(o)
                    else:
                        if o.type == "Attractor":
                            other.append(o)

        return walls, other, dropoff, pickup

    def update(self):
        inf = AnimateAction(None, None, None)

        if self.target.distance(self.body.location)<10:
            self.target = Vector2D(random.randint(0, 1000), random.randint(0, 1000))

        direction = Vector2D(self.target.x - self.body.location.x, self.target.y - self.body.location.y)

        self.velocity[0] += direction.x
        self.velocity[1] += direction.y

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)

        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move

        return inf

    def avoid_collisions(self, objs):
        # determine nearby objs using distance only

        c = [0.0, 0.0]
        for obj in objs:
            if hasattr(obj,"location"):
                diff = obj.location.x - self.body.location.x, obj.location.y - self.body.location.y
                facteur = ((util.magnitude(*diff) - 10) ** 2)
                if facteur != 0:
                    inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

                    c[0] = c[0] - inv_sqr_magnitude * diff[0]
                    c[1] = c[1] - inv_sqr_magnitude * diff[1]
            else:
                if hasattr(obj,"body"):
                    diff = obj.body.location.x - self.body.location.x, obj.body.location.y - self.body.location.y
                    facteur = ((util.magnitude(*diff) - 10) ** 2)
                    if facteur != 0:
                        inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

                        c[0] = c[0] - inv_sqr_magnitude * diff[0]
                        c[1] = c[1] - inv_sqr_magnitude * diff[1]

        return util.limit_magnitude(c, self.body.maxCollisionVel)

    def attraction(self, attractors):
        # generate a vector that moves the boid towards the attractors
        a = [0.0, 0.0]

        for attractor in attractors:
            a[0] += attractor.location.x - self.body.location.x
            a[1] += attractor.location.y - self.body.location.y

        return a


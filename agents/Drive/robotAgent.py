import random

from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.Drive.agentType import AgentType
from environment.application.Drive.robotBody import RobotBody
from helper import util
from helper.vector2D import Vector2D


class RobotAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.body = RobotBody()
        self.collisionDVel = 1
        self.type = AgentType.ROBOT
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.avoidanceFactor = 7.5
        self.obstacleFactor = 500
        self.target = Vector2D(0,0)

    def __init__(self, f=1):
        Agent.__init__(self)
        self.body = RobotBody()
        self.type = AgentType.ROBOT
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.avoidanceFactor = 7.5
        self.obstacleFactor = 500
        self.target = Vector2D(0, 0)

    def getEditable(self):
        return Agent.getEditable().append(["famille","avoidanceFactor",'obstacleFactor'])

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def filtrePerception(self):
        l = []
        other = []
        target = []

        return l, other, target

    def update(self):
        inf = AnimateAction(None, None, None)

        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move
        return inf

    def avoid_collisions(self, objs):
        # determine nearby objs using distance only

        c = [0.0, 0.0]
        for obj in objs:
            diff = obj.body.velocity.x - self.body.location.x, obj.body.velocity.y - self.body.location.y
            inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

            c[0] = c[0] - inv_sqr_magnitude * diff[0]
            c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return util.limit_magnitude(c, self.body.maxCollisionVel)

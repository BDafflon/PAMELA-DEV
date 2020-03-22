import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.DriveEnvironment.agentType import AgentType
from environment.application.DriveEnvironment.stardardAgentBody import StadardAgentBody
from helper import util
from helper.vector2D import Vector2D


class StandardAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.body = StadardAgentBody()
        self.collisionDVel = 1
        self.type =  AgentType.MANU
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0,0)

    def __init__(self, f):
        Agent.__init__(self)
        self.body = StadardAgentBody()
        self.type = AgentType.MANU
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0, 0)

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


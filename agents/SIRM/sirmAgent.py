import time
from random import random, randint

from agents.Drive.standardAgent import StandardAgent
from environment.animateAction import AnimateAction
from environment.application.Drive.agentState import AgentState

from environment.application.Drive.agentType import AgentType
from environment.application.Drive.stardardAgentBody import StadardAgentBody
from environment.application.SIRM.contamination import Contamination
from environment.application.SIRM.sickness import Sickness
from helper import util
from helper.vector2D import Vector2D


class SirmAgent(StandardAgent):
    def __init__(self):
        StandardAgent.__init__(self)
        self.body = StadardAgentBody()
        self.collisionDVel = 1
        self.type = AgentType.PATIENT
        self.stat=AgentState.SEIN
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 20
        self.body.vitesseMax = 15.0
        self.body.vitesseMin = 2.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0, 0)
        self.obstacleFactor = 0
        self.attractorFactor = 0.35
        self.contamination=None

    def __init__(self, f):
        StandardAgent.__init__(self,f)
        self.body = StadardAgentBody()
        self.type = AgentType.PATIENT
        self.famille = f
        self.body.fustrum.radius = 100
        self.contamination=None
        self.stat = AgentState.SEIN


    def filtrePerception(self):
        walls = []
        other = []
        dropoff = []
        pickup = []
        sick = []

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
                        '''else:
                            if o.type == AgentType.INFECTE:
                                sick.append(o)
                                other.append(o)
                            else:
                                if o.type == AgentType.RETABLI:
                                    other.append(o)
                                else:
                                    if o.type == AgentType.SEIN:
                                        other.append(o)'''

        return walls, other, dropoff, pickup, sick

    def moveTo(self, d):
        return Vector2D(d.location.x - self.body.location.x,
                        d.location.y - self.body.location.y)

    def moveRandom(self):
        x = int(randint(-2, 2))
        y = int(randint(-2, 2))
        return Vector2D(x, y)

    def update(self):
        influence = AnimateAction(None, None, None)

        walls, other, dropoff, pickp, sick = self.filtrePerception()
        sickness = Sickness()

        if self.type == AgentState.SEIN:
            influence.move = self.moveRandom()
        elif self.type == AgentState.INFECTE:
            influence.move = self.moveRandom()
        elif self.type == AgentState.QUARANTAINE:
            influence.move = self.moveRandom()
        elif self.type == AgentState.RETABLI:
            influence.move = self.moveRandom()



        self.velocity[0] += influence.move.x
        self.velocity[1] += influence.move.y

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        influence.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = influence.move
        return influence
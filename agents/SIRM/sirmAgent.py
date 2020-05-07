import time
from random import random, randint

from agents.Drive.standardAgent import StandardAgent
from environment.animateAction import AnimateAction
from environment.application.Drive.smirAgentState import SmirAgentState

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
        self.stat = SmirAgentState.SEIN
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 20
        self.body.vitesseMax = 15.0
        self.body.vitesseMin = 2.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0, 0)
        self.obstacleFactor = 500
        self.attractorFactor = 0.35
        self.contamination = None

    def __init__(self, f=1):
        StandardAgent.__init__(self, f)
        self.body = StadardAgentBody()
        self.type = AgentType.PATIENT
        self.famille = f
        self.body.fustrum.radius = 20
        self.contamination = None
        self.stat = SmirAgentState.SAIN

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
                        else:
                            if o.stat == SmirAgentState.INFECTE:
                                sick.append(o)
                                other.append(o)
                            else:
                                if o.stat == SmirAgentState.RETABLI:
                                    other.append(o)
                                else:
                                    if o.stat == SmirAgentState.SAIN:
                                        other.append(o)

        return walls, other, dropoff, pickup, sick

    def moveTo(self, d):
        return Vector2D(d.location.x - self.body.location.x,
                        d.location.y - self.body.location.y)

    def moveRandom(self):
        x = int(randint(-2, 2))
        y = int(randint(-2, 2))
        return Vector2D(x, y)

    def update(self):
        influence = AnimateAction(Vector2D(), Vector2D(), Vector2D())

        walls, other, dropoff, pickp, sick = self.filtrePerception()
        sickness = Sickness()

        if self.stat == SmirAgentState.SAIN:
            if len(sick) > 0:
                for s in sick:
                    if s.body.location.distance(self.body.location) < sickness.contagionRadius:
                        if (s.contamination.start + sickness.contagionStart) < time.time() < s.contamination.start + sickness.contagionStop:

                            r = randint(0, 100) / 100
                            if r < sickness.contagionFactor:
                                self.stat = SmirAgentState.INFECTE
                                s.contamination.nbContamination += 1
                                self.contamination = Contamination(time.time())

            influence.move = self.moveRandom()

        elif self.stat == SmirAgentState.INFECTE:
            influence.move = self.moveRandom()
            if (self.contamination.start + sickness.symptomeStart) < time.time():
                influence.move = self.moveTo(dropoff[0])
                if dropoff[0].aabb.inside(self.body.location):
                    self.stat =SmirAgentState.QUARANTAINE

            if self.contamination.start + sickness.mortalityTime < time.time():
                r = randint(0, 100) / 100
                if r < sickness.mortality:
                    self.stat = SmirAgentState.MORT
                else:
                    if (self.contamination.start + sickness.mortalityEnd) < time.time():
                        self.stat = SmirAgentState.RETABLI



        elif self.stat == SmirAgentState.QUARANTAINE:
            influence.move = self.moveRandom()
            if (self.contamination.start + sickness.contagionStop) < time.time():
                self.stat=SmirAgentState.RETABLI

        elif self.stat == SmirAgentState.RETABLI:
            influence.move = self.moveRandom()
        elif self.stat == SmirAgentState.MORT:
            influence.move=Vector2D()
            self.body.velocity = influence.move
            return influence


        self.velocity[0] += influence.move.x
        self.velocity[1] += influence.move.y

        obstacle_avoidance_vector = self.avoid_collisions(walls)

        self.velocity[0] += self.obstacleFactor * obstacle_avoidance_vector[0]
        self.velocity[1] += self.obstacleFactor * obstacle_avoidance_vector[1]

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        influence.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = influence.move
        return influence

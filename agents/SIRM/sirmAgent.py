import time
from random import random, randint

from agents.Drive.standardAgent import StandardAgent
from environment.animateAction import AnimateAction

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
        self.type = AgentType.MANU
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
        self.type = AgentType.MANU
        self.famille = f
        self.body.fustrum.radius = 100
        self.contamination=None


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
                            if o.type == AgentType.INFECTE:
                                sick.append(o)
                                other.append(o)
                            else:
                                if o.type == AgentType.RETABLI:
                                    other.append(o)
                                else:
                                    if o.type == AgentType.SEIN:
                                        other.append(o)

        return walls, other, dropoff, pickup, sick

    def update(self):
        inf = AnimateAction(None, None, None)

        walls, other, dropoff, pickp, sick = self.filtrePerception()

        sickness = Sickness()
        if self.type == AgentType.INFECTE and (self.contamination.start + sickness.mortalityEnd)<time.time() :
            self.type = AgentType.RETABLI
        if self.type == AgentType.INFECTE and (self.contamination.start + sickness.mortalityTime)<time.time() :
            r = randint(0, 100) / 100
            if r < sickness.mortality :
                self.type = AgentType.MORT

        if len(sick)> 0 and self.type == AgentType.SEIN:
            for s in sick:
                if (s.contamination.start + sickness.contagionStart) < time.time() < s.contamination.start + sickness.contagionStop:

                    r = randint(0, 100) / 100
                    if r<sickness.contagionFactor :
                        self.type = AgentType.INFECTE
                        s.contamination.nbContamination+=1
                        self.contamination = Contamination(time.time())



        obstacle_avoidance_vector = self.avoid_collisions(other)
        #attractor_vector = self.attraction(other)

        self.velocity[0] += self.obstacleFactor * obstacle_avoidance_vector[0]
        self.velocity[1] += self.obstacleFactor * obstacle_avoidance_vector[1]

        #self.velocity[0] += self.attractorFactor * attractor_vector[0]
        #self.velocity[1] += self.attractorFactor * attractor_vector[1]

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move
        return inf
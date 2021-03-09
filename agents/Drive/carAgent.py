import random

from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.Drive.agentType import AgentType
from environment.application.Drive.stardardAgentBody import StadardAgentBody
from helper import util
from helper.vector2D import Vector2D


class CarAgent(Agent):

    def __init__(self, f=1):
        Agent.__init__(self)
        self.body = StadardAgentBody()
        self.type = AgentType.CAR
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 10
        self.body.vitesseMax = 200.0
        self.body.vitesseMin = 1.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0, 0)


        self.name='car'

    def getEditable(self):
        return Agent.getEditable().append(["famille","avoidanceFactor",'obstacleFactor','type'])




        return Vector2D(x, y)

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
        print(self.wayPoint[self.startWayPoint])
        vec = Vector2D(self.wayPoint[self.startWayPoint][0],self.wayPoint[self.startWayPoint][1])
        if vec.distance(self.body.location)<10:
            self.startWayPoint=(self.startWayPoint+1)%len(self.wayPoint)


        inf = AnimateAction(None, None, None)

        direction = Vector2D(vec.x-self.body.location.x,vec.y-self.body.location.y)

        self.velocity[0] += direction.x
        self.velocity[1] += direction.y

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)

        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move

        return inf




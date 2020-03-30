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
        self.type = AgentType.MANU
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.target = Vector2D(0, 0)
        self.obstacleFactor = 500

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
        self.obstacleFactor = 500

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

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
                        other.append(o)

        return walls, other, dropoff, pickup

    def update(self):
        inf = AnimateAction(None, None, None)

        walls, other, dropoff, pickp = self.filtrePerception()
        obstacle_avoidance_vector = self.avoid_collisions(walls)

        self.velocity[0] += self.obstacleFactor * obstacle_avoidance_vector[0]
        self.velocity[1] += self.obstacleFactor * obstacle_avoidance_vector[1]

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
                inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

                c[0] = c[0] - inv_sqr_magnitude * diff[0]
                c[1] = c[1] - inv_sqr_magnitude * diff[1]

        return util.limit_magnitude(c, self.body.maxCollisionVel)

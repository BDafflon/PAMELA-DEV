from environment.application.DriveEnvironment import agentType
from environment.environment import Environment
import time
from helper.vector2D import Vector2D


class EnvironmentDrive(Environment):
    def __init__(self):
        Environment.__init__(self)

    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                return a
        return None

    def getFirstRobot(self):
        return self.getRandomAgent(agentType.ROBOT)

    def update(self, dt):
        self.clock = (time.time())

        self.influenceList = {}

        for agent in self.agents:
            self.computePerception(agent)

        for agent in self.agents:
            self.influenceList[agent.id] = None
            self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)
        #print("dt : " + str(dt))

    def applyInfluence(self, dt):
        actionList = {}
        for k, influence in self.influenceList.items():

            if influence == None:
                continue

            agentBody = self.getAgentBody(k)

            if not agentBody is None:
                move = Vector2D(influence.move.x, influence.move.y)
                rotation = 0
                move = agentBody.computeMove(move)
                move = move.scale(dt)
                agentBody.move(move)
                self.edges(agentBody)

    def edges(self,b):

        if b.location.x > self.boardW:
            b.location.x = 1
        elif b.location.x < 0:
            b.location.x = b.location.x % self.boardW-1

        if b.location.y > self.boardH:
            b.location.y = 1
        elif b.location.y < 0:
            b.location.y = b.location.y % self.boardH-1
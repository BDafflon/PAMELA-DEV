from random import randint

from environment.application.Drive import agentType
from environment.application.Drive.agentState import AgentState
from environment.application.Drive.agentType import AgentType
from environment.environment import Environment
import time

from helper import util
from helper.vector2D import Vector2D


class EnvironmentDrive(Environment):
    def __init__(self):
        Environment.__init__(self)




    def addAgent(self, a):
        if 'quarantaine' in self.zone.keys():
            if self.zone['quarantaine'].inside(a.body.location):
                a.body.location = Vector2D(self.boardW/2,self.boardH/2)
        self.agents.append(a)

    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                return a
        return None

    def getFirstRobot(self):
        return self.getRandomAgent(agentType.ROBOT)


    def getPopulation(self):
        data={}
        for d in AgentState:
            data[d]=0

        for a in self.agents:

            if a.stat in data.keys():
                data[a.stat]=data[a.stat]+1
            else:
                data[a.stat]=1

        return data

    def getContent(self,point2d):
        for o in self.objects:
            if hasattr(o,'aabb'):
                if o.aabb.inside(point2d):
                    txt = o.type +" "+str(o.id)+" "+str(o.aabb.uperLeftLocation.y)+" :\n"
                    if hasattr(o, 'stock'):
                        if(len(o.stock)>0):

                            txt=txt+ '\n'.join(map(str, o.stock))
                        return txt

    def update(self, dt):
        self.influenceList = {}

        for agent in self.agents:
            if agent.stat == AgentState.QUARANTAINE and not self.zone['quarantaine'].inside(agent.body.location):
                self.moveTo(agent,"quarantaine")

            if agent.stat != AgentState.MORT:
                self.computePerception(agent)

        for agent in self.agents:
            if agent.stat != AgentState.MORT:
                self.influenceList[agent.id] = None
                self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)

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

    def insideWall(self, a):
        for i in self.objects:
            if i.type == "Wall":
                inside = i.aabb.inside(a.body.location)
                print ("inside")
                return inside
        return False
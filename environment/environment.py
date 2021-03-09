import ctypes
import multiprocessing
import threading
import time
from random import randint

from environment.application.Drive.agentType import AgentType
from environment.object import PerceivedObject
from helper import util
from helper.datastructure import kdtree
from helper.util import chunkIt
from helper.vector2D import Vector2D


class clock:
    def __init__(self):
        self.t=0

c= clock()

class Environment(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.boardW = 100000
        self.boardH = 100000
        self.running = 1
        self.clock=0
        self.agents = []
        self.objects = []
        self.perceptionList = {}
        self.influenceList = {}
        self.zone={}
        self.tree = None


    def addAgent(self, a):
        self.agents.append(a)


    def addObject(self, o):
        self.objects.append(o)

    def getContent(self,point2d):
        for o in self.objects:
            if hasattr(o,'aabb'):
                if o.aabb.inside(point2d):
                    txt = str(o)
                    return txt
        return ""
    def getPopulation(self):
        data={}
        for d in AgentType:
            data[d]=0

        for a in self.agents:
            if a.type in data.keys():
                data[a.type]=data[a.type]+1
            else:
                data[a.type]=1

        return data

    def moveTo(self,a,zone):
        if zone in self.zone.keys() :
            a.body.location=Vector2D(randint(self.zone[zone].uperLeftLocation.x,self.zone[zone].uperLeftLocation.x+self.zone[zone].width),randint(self.zone[zone].uperLeftLocation.y,self.zone[zone].uperLeftLocation.y+self.zone[zone].height))

    def getRandomObject(self, typeO):
        while True:
            d = util.randomInt(len(self.objects))
            if self.objects[d].type == typeO:
                return self.objects[d]

    def getFirstObjectByName(self, type):
        for o in self.objects:
            if o.type == type:
                return o
        return None

    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                return a
        return None

    def subUpdate(self,agent):
        print("sub")
        if not agent.kill:
            self.computePerception(agent)
            self.influenceList[agent.id] = None
            self.influenceList[agent.id] = agent.update()


    def update(self, dt):

        self.clock = (time.time())
        self.influenceList = {}
        if len(self.agents)>0:
            self.tree = kdtree.create(self.agents)
        for agent in self.agents:
            if not agent.kill :
                self.computePerception(agent)
                self.influenceList[agent.id] = None
                self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)
        #print(time.time() - self.clock)




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

    def edges(self, b):
        if b.location.x > self.boardW:
            b.location.x = 1
        elif b.location.x < 0:
            b.location.x = b.location.x % self.boardW - 1

        if b.location.y > self.boardH:
            b.location.y = 1
        elif b.location.y < 0:
            b.location.y = b.location.y % self.boardH - 1





    def computePerception(self, a):

        self.perceptionList[a] = []

        if self.tree is not None:
            n = self.tree.search_nn_dist(a, a.body.fustrum.radius)
            self.perceptionList[a] = n


        for objet in self.objects:

            if hasattr(objet,"aabb"):
                if objet.type == "Dropoff":
                    self.perceptionList[a].append(PerceivedObject(objet.location, objet.aabb, objet.type))

                if hasattr(a.body.fustrum,"radius"):
                    collision,point = objet.aabb.intersection(a.body.location, a.body.fustrum.radius)
                    if collision:
                        self.perceptionList[a].append(PerceivedObject(objet.location, objet.aabb, objet.type))

            else :
                if a.body.insidePerception(objet.location):
                    self.perceptionList[a].append(objet)

        a.body.fustrum.perceptionList = self.perceptionList[a]


    def getAgentBody(self, k):
        for a in self.agents:
            if a.id == k:
                return a.body
        return None

    def getAgent(self, k):
        for a in self.agents:
            if a.id == k:
                return a
        return None

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

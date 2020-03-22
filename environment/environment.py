from helper import util
import time
from helper.vector2D import Vector2D
import threading
import ctypes


class Environment(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.center=Vector2D(800/2,600/2)
        self.boardW = 1280
        self.boardH = 720
        self.running = 1
        self.clock=0
        self.agents = []
        self.objects = []
        self.perceptionList = {}
        self.influenceList = {}

    def addAgent(self, a):
        self.agents.append(a)

    def addObject(self, o):
        self.objects.append(o)

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

    def update(self, dt):
        self.clock = (time.time())

        self.influenceList = {}

        for agent in self.agents:
            self.computePerception(agent)

        for agent in self.agents:
            self.influenceList[agent.id] = None
            self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)
        # print("dt : " + str(dt))

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
        for agent in self.agents:
            if agent != a:
                if a.body.insidePerception(agent.body.location, agent.type):
                    self.perceptionList[a].append(agent)

        for objet in self.objects:
            if a.body.insidePerception(objet.location, agent.type):
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

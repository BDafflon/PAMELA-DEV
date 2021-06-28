
import json
import random
import threading
import time

from agents.agent import Agent
from environment.environment import Environment
from environment.object import Object
from helper import util
from helper.BoundingBox.aabb import AABB
from helper.drawPopulation import drawPopulation
from helper.importer.driveImporter import importationIMG, importationJSON
from helper.util import inspectAgentsDict
from helper.vector2D import Vector2D


class SimulationMas(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        try:
            self.drawPopulation = False
            self.environment = Environment()
            self.ready = False
            self.event = []
            self.limitSimulation = 600
            self.pause = False
            self.end=False
        except Exception as e:
            print(e)

    def loadDefault(self):
        self.ready = True


    def loadEnvironment(self,f):
        objetList=[]
        if f.endswith('.json'):
            objetList = importationJSON(f)
        else :
            if f.endswith('.jpg') or f.endswith('.bmp') or f.endswith('.png'):
                objetList = importationIMG(f)

        if len(objetList)>0:
            self.parseJson(objetList)


    def parseJson(self,jsonSim):
        try:
            if "start" in jsonSim:
                start = jsonSim["start"]

                for e in start:
                    if "entity" in e:
                        if e["entity"] == "agent":
                            n = inspectAgentsDict(Agent)
                            if "type" in e:
                                nb=1
                                if "number" in e:
                                    nb = int(e['number'])

                                for na in range(0,nb):
                                    a = n[e['type']]()
                                    if "id" in e:
                                        a.id = e['id']+str(random.randint(100,100000))
                                    if "position" in e:
                                        a.body.location = Vector2D(e["position"][0], e["position"][1])
                                    if "randomPosision" in e:
                                        a.body.location = Vector2D(
                                            util.randomRangeInt(e["randomPosision"][0][0], e["randomPosision"][0][1]),
                                            util.randomRangeInt(e["randomPosision"][1][0], e["randomPosision"][1][1]))
                                    if "customArgs" in e:
                                        for key, value in e["customArgs"].items():
                                            setattr(a, key, value)
                                    self.environment.addAgent(a)
                        else:
                            if e["entity"] == "object":

                                n = inspectAgentsDict(Object)
                                if "type" in e:
                                    o = n[e["type"]]()
                                    if "name" in e:
                                        o.name = e["name"]
                                    if "aabb" in e:
                                        if hasattr(o, 'aabb'):
                                            o.aabb = AABB(Vector2D(e["aabb"][0], e["aabb"][1]), e["aabb"][2], e["aabb"][3])
                                    if "customArgs" in e:
                                        for key, value in e["customArgs"].items():
                                            setattr(o, key, value)
                                self.environment.addObject(o)
                                if len(self.environment.objects) == 43:
                                    print("43")
                                print(len(self.environment.objects))

                            else:
                                if e["entity"] == "zone":
                                    if "name" in e and "aabb" in e:
                                        self.environment.zone[e['name']] = AABB(Vector2D(e["aabb"][0], e["aabb"][1]),
                                                                                e["aabb"][2], e["aabb"][3])

            if "simulation" in jsonSim:
                simulation = jsonSim["simulation"]
                for e in simulation:
                    if "entity" in e:
                        if e["entity"] == "agent":
                            n = inspectAgentsDict(Agent)
                            if "type" in e:
                                a = n[e['type']]()
                                if "id" in e:
                                    a.id = e['id']
                                if "position" in e:
                                    a.body.location = Vector2D(e["position"][0], e["position"][1])
                                if "randomPosision" in e:
                                    a.body.location = Vector2D(
                                        util.randomRangeInt(e["randomPosision"][0][0], e["randomPosision"][0][1]),
                                        util.randomRangeInt(e["randomPosision"][1][0], e["randomPosision"][1][1]))
                                if "customArgs" in e:
                                    for key, value in e["customArgs"].items():
                                        setattr(a, key, value)
                                self.event.append({"time": e["timelaunch"], 'type': "agent", 'event': a})
                        else:
                            if e["entity"] == "object":

                                n = inspectAgentsDict(Object)
                                if "type" in e:
                                    o = n[e["type"]]()
                                    if "name" in e:
                                        o.name = e["name"]
                                    if "aabb" in e:
                                        if hasattr(o, 'aabb'):
                                            o.aabb = AABB(Vector2D(e["aabb"][0], e["aabb"][1]), e["aabb"][2], e["aabb"][3])
                                    if "customArgs" in e:
                                        for key, value in e["customArgs"].items():
                                            setattr(a, key, value)
                                    self.event.append({"time": e["timelaunch"], 'type': 'objet', 'event': o})
                            else:
                                if e["entity"] == "zone":

                                    if "name" in e and "aabb" in e:
                                        z = AABB(Vector2D(e["aabb"][0], e["aabb"][1]), e["aabb"][2], e["aabb"][3])
                                        self.event.append(
                                            {"time": e["timelaunch"], 'type': 'zone', 'name': e['name'], 'event': z})

        except Exception as e:
            print("exception",e)
        self.ready=True

    def loadScenario(self,f):
        print(f)
        try:
            with open(f, 'r') as f:
                jsonSim = json.load(f)

            self.parseJson(jsonSim)
            self.ready = True
            if "configuration" in jsonSim:

                return 1,"OK",jsonSim["configuration"]
            else:
                return 1,"OK",{}


        except Exception as e:  # work on python 3.x
            print("Fichier non compatible")
            return -1,"Fichier non compatible", repr(e)


    def run(self):
        print("Run scenario")
        if self.ready:
            if self.drawPopulation:
                drawPopulation(self.environment)
            # TODO Scenario
            print("=====================Scenario START =====================")
            print("=====================Events :",len(self.event)," =====================")
            iterator = 0;
            startTime = int(time.time())
            elapseTime = 0


            while iterator < len(self.event):

                try:
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
                print(iterator)
                if self.pause:
                    startTime = int(time.time()) + elapseTime
                else :
                    elapseTime = int(time.time()) - startTime

                    if elapseTime % 10 == 0:
                        print("====================="+str(int(iterator*100/len(self.event)))+"%=====================")
                    if elapseTime > self.limitSimulation:
                        iterator = len(self.event)

                    else:
                        if elapseTime > self.event[iterator]["time"]:

                            if self.event[iterator]['type']== 'agent':
                                self.environment.addAgent(self.event[iterator]['event'])
                                print("-- Agent spawned")
                                iterator+=1
                            else :
                                if self.event[iterator]['type'] == 'objet':
                                    self.environment.addObject(self.event[iterator]['event'])
                                    iterator += 1
                                    print("-- Object spawned")
                                else:
                                    if self.event[iterator]['type'] == 'zone':
                                        self.environment.zone[self.environment[iterator]['name']]=self.environment[iterator]['event']
                                        print("-- Zone created")
                                        iterator += 1

            print("===================== Scenario END =====================")
            self.end=True




        else:
            print("Erreur de simulation")


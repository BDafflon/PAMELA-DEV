import csv
import threading
import time
import tkinter

from agents.Drive.robotAgent import RobotAgent
from agents.Drive.standardAgent import StandardAgent
from agents.SIRM.sirmAgent import SirmAgent
from environment.application.Drive.agentState import AgentState
from environment.application.Drive.agentType import AgentType

from environment.application.Drive.environmentDrive import EnvironmentDrive
from environment.application.SIRM.contamination import Contamination

from environment.object import TargetObjet, Dropoff, Pickup, Wall
from helper.BoundingBox.aabb import AABB
from helper.importer.configurator import Configurator
from helper.importer.driveImporter import importationIMG, importationJSON
from helper.drawPopulation import drawPopulation, Afficheur
from helper.vector2D import Vector2D, randint


class SIRMSimulation(threading.Thread):
    def __init__(self, pathEnv, pathScenario, pathStock):
        threading.Thread.__init__(self)
        self.drawPopulation = False
        self.environment = EnvironmentDrive()
        self.pathEnv = pathEnv
        self.pathStock = pathStock
        self.pathScenario = pathScenario
        self.ready = False

    def loadDefault(self):

        objetList = []
        if self.pathEnv.endswith('.json'):
            objetList = importationJSON(self.pathEnv)
        else :
            if self.pathEnv.endswith('.jpg') or self.pathEnv.endswith('.bmp') or self.pathEnv.endswith('.png'):
                objetList,dim = importationIMG(self.pathEnv)
                self.environment.boardW = dim[1]
                self.environment.boardH = dim[0]

            else:
                print("Fichier environement incompatible")


        j = 0
        k = 0
        pickupList = []
        for i in objetList:
            if i['type'] == "zone":
                x = i['coord'][0]
                y = i['coord'][1]
                w = i['coord'][2]
                h = i['coord'][3]
                self.environment.zone[i['name']] = AABB(Vector2D(x, y), h, w)
            else:
                x = i['coord'][0]
                y = i['coord'][1]
                w = i['coord'][2]
                h = i['coord'][3]

                if i['type'] == "dropoff":
                    j = j + 1
                    self.environment.addObject(Dropoff(x, y, h, w, j))
                else:
                    if i['type'] == "pickup":
                        k = k + 1
                        a = Pickup(x, y, h, w, k)
                        pickupList.append(a)
                        self.environment.addObject(a)
                    else:
                        if i['type'] == "wall":
                            self.environment.addObject(Wall(x, y, h, w))
                        else:
                            if i['type'] == "environement":
                                self.environment.boardW = w
                                self.environment.boardH = h



        stock = self.loadStock()

        i = 0
        if len(pickupList) > 0:
            for r in stock:
                pickupList[i % len(pickupList)].stock.append(r)
                i = i + 1

        self.environment.addObject(TargetObjet(0, 0))

        for i in range(0, 100):
            a = SirmAgent(1)
            a.body.location = Vector2D(randint(0, self.environment.boardW), randint(0, self.environment.boardH))
            a.stat = AgentState.SEIN
            self.environment.addAgent(a)


        self.ready = True

    def run(self):

        if self.ready:
            self.environment.start()
            if self.drawPopulation:
                a = Afficheur(self.environment)
                a.start()
            # TODO Scenario
            limit = 10
            start=time.time()
            i=0

            while i<limit:
                i+=1

                a = SirmAgent(1)
                a.body.location = Vector2D(randint(200, 250), randint(200, 250))
                a.stat = AgentState.INFECTE
                a.contamination = Contamination(time.time())
                self.environment.addAgent(a)
                time.sleep(5)

        else:
            print("Erreur de simulation")

    def loadStock(self):
        stock = []

        if self.pathStock.endswith('.csv'):
            line_count = 0



            with open(self.pathStock) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for row in csv_reader:

                    if row[0] != '':
                        stock.append([row[0], int(row[1])])
        else:
            print("Erreur : fichier stock incompatible")
        return stock

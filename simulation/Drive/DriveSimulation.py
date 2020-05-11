import csv
import threading
import tkinter

from agents.Drive.robotAgent import RobotAgent
from agents.Drive.standardAgent import StandardAgent
from environment.application.Drive.environmentDrive import EnvironmentDrive
from environment.object import TargetObjet, Dropoff, Pickup, Wall
from helper.drawPopulation import drawPopulation
from helper.importer.configurator import Configurator
from helper.importer.driveImporter import importationIMG, importationJSON


class DriveSimulation(threading.Thread):
    def __init__(self, pathEnv, pathScenario, pathStock):
        threading.Thread.__init__(self)
        self.drawPopulation = False
        self.environment = EnvironmentDrive()
        self.pathEnv = pathEnv
        self.pathStock = pathStock
        self.pathScenario = pathScenario
        self.ready = False

    def loadDefault(self):
        if self.pathEnv == "" or self.pathScenario == "" or self.pathStock == "":
            configurator = Configurator(tkinter.Tk(),self.pathEnv,self.pathStock,self.pathScenario)
            self.pathEnv,self.pathStock,self.pathScenario = configurator.getFile()

        objetList = []
        if self.pathEnv.endswith('.json'):
            objetList = importationJSON(self.pathEnv)
        else :
            if self.pathEnv.endswith('.jpg') or self.pathEnv.endswith('.bmp') or self.pathEnv.endswith('.png'):
                objetList = importationIMG(self.pathEnv)
            else:
                print("Fichier environement incompatible")



        #print(objetList)
        j = 0
        k = 0
        pickupList = []
        for i in objetList:

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

        stock = self.loadStock()

        i = 0
        if len(pickupList) > 0:
            for r in stock:
                pickupList[i % len(pickupList)].stock.append(r)
                i = i + 1

        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 10):
            self.environment.addAgent(StandardAgent(1))


        for i in range(0, 10):
            self.environment.addAgent(RobotAgent(1))

        self.ready = True

    def run(self):

        if self.ready:
            self.environment.start()
            if self.drawPopulation:
                drawPopulation(self.environment)
            # TODO Scenario

        else:
            print("Erreur de simulation")

    def loadStock(self):
        stock = []

        if self.pathStock.endswith('.csv'):
            line_count = 0

            print("Load Stock " + self.pathStock)

            with open(self.pathStock) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for row in csv_reader:

                    if row[0] != '':
                        stock.append([row[0], int(row[1])])
        else:
            print("Erreur : fichier stock incompatible")
        return stock

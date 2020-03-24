import csv
import threading
import time

from agents.Drive.robotAgent import RobotAgent
from agents.Drive.standardAgent import StandardAgent
from environment.application.DriveEnvironment.environmentDrive import EnvironmentDrive

from environment.object import TargetObjet, Dropoff, Pickup, Wall
from helper.importer.driveImporter import importation


class DriveSimulation(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)






        self.environment = EnvironmentDrive()
        self.path = path
        self.ready = False

    def loadDefault(self):
        objetList = importation()
        j=0
        for i in objetList:
            print(i)

        print('----')
        for i in objetList:

            x = i['coord'][0]
            y = i['coord'][1]
            w = i['coord'][2]
            h = i['coord'][3]

            if i['type'] == "dropoff":
                self.environment.addObject(Dropoff(x, y, h, w))
            else :
                if i['type'] == "pickup":
                    self.environment.addObject(Pickup(x, y, h, w))
                else :
                    if i['type'] == "wall" and j<40:
                        j=j+1
                        print(i)
                        self.environment.addObject(Wall(x, y, h, w))

        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 10):
            self.environment.addAgent(StandardAgent(1))

        for i in range(0, 2):
            self.environment.addAgent(RobotAgent(1))

        self.ready = True

    def run(self):
        if self.ready:
            self.environment.start()
        else:
            print("Erreur de simulation")

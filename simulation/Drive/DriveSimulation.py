import csv
import threading
import time

from agents.Drive.robotAgent import RobotAgent
from agents.Drive.standardAgent import StandardAgent
from environment.application.DriveEnvironment.environmentDrive import EnvironmentDrive

from environment.object import TargetObjet


class DriveSimulation(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.environment = EnvironmentDrive()
        self.path = path
        self.ready = False

    def loadDefault(self):
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

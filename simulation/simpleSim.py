import csv
import threading
import time
import tkinter

from agents.Drive.robotAgent import RobotAgent
from agents.Drive.standardAgent import StandardAgent
from environment.application.Drive.environmentDrive import EnvironmentDrive
from environment.environment import Environment

from environment.object import TargetObjet, Dropoff, Pickup, Wall
from helper.importer.configurator import Configurator
from helper.importer.driveImporter import importationIMG, importationJSON
from helper.drawPopulation import drawPopulation


class SimpleSimulation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.drawPopulation = False
        self.environment = Environment()
        self.ready = False

    def loadDefault(self):

        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 100):
            self.environment.addAgent(StandardAgent(1))

        self.ready = True

    def run(self):

        if self.ready:
            self.environment.start()
            if self.drawPopulation:
                drawPopulation(self.environment)
            # TODO Scenario

        else:
            print("Erreur de simulation")


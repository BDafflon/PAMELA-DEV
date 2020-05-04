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
from simulation.simulation import Simulation


class SimpleSimulation(Simulation):
    def __init__(self):
        Simulation.__init__(self)


    def loadDefault(self):

        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 100):
            self.environment.addAgent(StandardAgent(1))

        self.ready = True


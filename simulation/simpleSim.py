from agents.Drive.standardAgent import StandardAgent

from environment.object import TargetObjet
from simulation.simulation import Simulation


class SimpleSimulation(Simulation):
    def __init__(self):
        Simulation.__init__(self)


    def loadDefault(self):

        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 100):
            self.environment.addAgent(StandardAgent(1))

        self.ready = True


import test

from agents.Drive.standardAgent import StandardAgent
from environment.environment import Environment
from gui.guiDrivegl import GuiDriveGL
from gui.pamelaView import PamGui
from simulation.Drive.DriveSimulation import DriveSimulation
from simulation.SIRM.SIRMSimulation import SIRMSimulation
from simulation.simpleSim import SimpleSimulation


def runDriveSimulation(pathEnv, pathSce, pathStock):
    s = DriveSimulation(pathEnv, pathSce, pathStock)
    s.drawPopulation = False
    s.loadDefault()

    g = GuiDriveGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []

def runSimpleSimulation(pathEnv, pathSce, pathStock):
    s = SimpleSimulation()


    s.loadDefault()

    g = PamGui(s)
    s.Gui = g
    s.start()
    g.run2()
    g.stop2()


def runSIRMSimulation(pathEnv, pathSce, pathStock):
    s = SIRMSimulation(pathEnv, pathSce, pathStock)
    s.drawPopulation = False
    s.loadDefault()


    g = PamGui(s)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []

runSimpleSimulation("", ".\\simulation\\Drive\\drive.csv", ".\\simulation\\Drive\\stock.csv")


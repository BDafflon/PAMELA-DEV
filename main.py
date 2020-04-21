from gui.guiDrivegl import GuiDriveGL
from simulation.Drive.DriveSimulation import DriveSimulation
from simulation.SIRM.SIRMSimulation import SIRMSimulation


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

def runSIRMSimulation(pathEnv, pathSce, pathStock):
    s = SIRMSimulation(pathEnv, pathSce, pathStock)
    s.drawPopulation = False
    s.loadDefault()

    g = GuiDriveGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []

runSIRMSimulation(".\\helper\\importer\\env.json", ".\\simulation\\Drive\\drive.csv", ".\\simulation\\Drive\\stock.csv")


from gui.guiDrivegl import GuiDriveGL
from simulation.Drive.DriveSimulation import DriveSimulation

def runDriveSimulation(pathEnv, pathSce, pathStock):
    s = DriveSimulation(pathEnv, pathSce, pathStock)

    s.loadDefault()

    g = GuiDriveGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []


runDriveSimulation(".\\helper\\importer\\env.json", ".\\simulation\\Drive\\drive-25-03-20.csv", ".\\simulation\\Drive\\stock.csv")


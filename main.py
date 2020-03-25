from gui.guiDrivegl import GuiDriveGL
from helper.importer.driveImporter import importation

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


runDriveSimulation("C:\\Users\\baudo\\PycharmProjects\\PAMELA-DRIVE\\helper\\importer\\drive1.bmp",
                   "C:\\Users\\baudo\\PycharmProjects\\PAMELA-DRIVE\\simulation\\Drive\\drive-25-03-20.csv", "C:\\Users\\baudo\\PycharmProjects\\PAMELA-DRIVE\\simulation\\Drive\\stock.csv")


from gui.guiDrivegl import GuiDriveGL
from helper.importer.driveImporter import importation

from simulation.Drive.DriveSimulation import DriveSimulation





def runSIRMSimulation(path):
    s = DriveSimulation(path)

    s.loadDefault()

    g = GuiDriveGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []


runSIRMSimulation("")

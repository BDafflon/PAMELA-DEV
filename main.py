
from gui.guiDrivegl import GuiDriveGL

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

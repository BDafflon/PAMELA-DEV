import math
from math import sqrt

import shapely as shapely

from gui.guiDrivegl import GuiDriveGL
from helper import util
from helper.BoundingBox import aabb
from helper.BoundingBox.aabb import AABB
from helper.importer.driveImporter import importation
from helper.util import getIntersectionPoint, distance
from helper.vector2D import Vector2D

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


runDriveSimulation(".\\helper\\importer\\drive1.bmp", ".\\simulation\\Drive\\drive-25-03-20.csv", ".\\simulation\\Drive\\stock.csv")


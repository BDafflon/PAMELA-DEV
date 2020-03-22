import csv
from csv import *


class ObserverManager:
    def __init__(self, pathDir):
        self.observer = []
        self.pathDir = pathDir

    def addObservation(self, o):
        self.observer.append(o)

    def removeObserver(self, o):
        self.observer.remove(o)

    def write(self):
        fileRobot = open(self.pathDir+"/robot.csv", "w")


        try:
            writerRobot = csv.writer(fileRobot, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)



            writerRobot.writerow(["id ", "id deplacement", "heure de départ (s)","distance(m)", "temps de deplacement(s)","nombre de colis"])

            #
            # Écriture des quelques données.

            for l in self.observer:
                if l.type=="Robot":
                    writerRobot.writerow([l.id,l.idDeplacement,l.HDepart,l.distance,l.temps,l.nbPassager])
        finally:
            #
            # Fermeture du fichier source
            #
            fileRobot.close()


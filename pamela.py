from gui.pamelaView import PamGui
from simulation.simulation import SimulationMas

print("start")

def runSimpleSimulation(pathEnv=""):
    s = SimulationMas()
    s.loadEnvironment(pathEnv)
    g = PamGui(s)
    s.Gui = g
    s.run()



if __name__ =="__main__":
    runSimpleSimulation("./scenario/test.json")


import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import sys
from threading import Thread
import time

data = []
def update(i,   dataEnv):
    j = 0

    for d in dataEnv:
        if len(data) <= j:
            data.append([])
        data[j].append(dataEnv[d])
        j = j + 1

    return data, dataEnv.keys()


def animate(j, data, env):
    x = [i for i in range(0, j)]

    if j > 0:
        dataEnv = env.getPopulation()
        data, k = update(j,  dataEnv)

        plt.cla()
        width = 0.35


        plt.stackplot(x, data, labels=k)
        plt.legend(loc='upper left')

        plt.tight_layout()


def drawPopulation(env):


    ani = FuncAnimation(plt.gcf(), animate, fargs=(data, env,), interval=1000)

    plt.tight_layout()
    plt.show()



class Afficheur(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, env):
        Thread.__init__(self)
        self.env = env

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""

        drawPopulation(self.env)

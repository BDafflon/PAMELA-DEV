import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def update(i, data, dataEnv):
    j = 0

    for d in dataEnv:
        if len(data) <= j:
            data.append([])
            data[j].append(dataEnv[d])
        j = j + 1
    print(data)
    return data, dataEnv.keys()


def animate(j, data, env):
    x = [i for i in range(0, j)]

    if j > 0:
        dataEnv = env.getPopulation()
        data, k = update(j, data, dataEnv)

        plt.cla()
        width = 0.35


        plt.stackplot(x, data, labels=k)
        plt.legend(loc='upper left')

        plt.tight_layout()

data = []
def drawPopulation(env):
    plt.style.use('fivethirtyeight')

    ani = FuncAnimation(plt.gcf(), animate, fargs=(data, env,), interval=1000)

    plt.tight_layout()
    plt.show()

import random

from environment.body import Body
from helper import util
from helper.observer import Observer


class Agent:
    def __init__(self):
        self.velocity = random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)
        self.id = util.id_generator(10, "123456789")
        self.type = "Agent"
        self.body = Body()
        self.stat = 0
        self.observer = Observer(self.id,"Agent")
        self.kill = False

    def update(self):
        print(self.id)
        print(len(self.body.fustrum.perceptionList))

    def getEditable(self):
        return ['id']

        # KDTREE
    def __len__(self):
        return 2

    def __getitem__(self, i):
        if i == 0:
            return self.body.location.x
        else:
            return self.body.location.y

    def __repr__(self):
        return 'Agent({}, {}, {})'.format(self.body.location.x, self.body.location.y, self.id)

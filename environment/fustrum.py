class Fustrum:
    def __init__(self):
        self.type = "fustrum"
        self.perceptionList = []


class CircularFustrum(Fustrum):
    def __init__(self):
        Fustrum.__init__(self)
        self.radius = 10
        self.angle = 180

    def __init__(self, r):
        Fustrum.__init__(self)
        self.radius = r
        self.angle = 180

    def inside(self, pBody, pObject):
        if pBody.distance(pObject) < self.radius:
            return True

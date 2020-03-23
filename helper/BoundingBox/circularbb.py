from helper.BoundingBox.boundingBox import BoundingBox


class CircularBoundingBox(BoundingBox):
    def __init__(self):
        BoundingBox.__init__(self)
        self.radius = 1

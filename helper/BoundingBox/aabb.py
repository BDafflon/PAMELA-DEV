from helper.BoundingBox.boundingBox import BoundingBox
from helper.vector2D import Vector2D


class AABB(BoundingBox):
    def __init__(self):
        BoundingBox.__init__(self)
        self.uperLeftLocation = Vector2D(0,0)
        self.height=1
        self.width=1
from helper.BoundingBox.boundingBox import BoundingBox
from helper.vector2D import Vector2D


class AABB(BoundingBox):
    def __init__(self,l,h,w):
        BoundingBox.__init__(self)
        self.uperLeftLocation = l
        self.height=h
        self.width=w
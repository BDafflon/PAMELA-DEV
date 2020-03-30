from helper.BoundingBox.boundingBox import BoundingBox
from helper.util import distance
from helper.vector2D import Vector2D


class AABB(BoundingBox):
    def __init__(self, l, h, w):
        BoundingBox.__init__(self)
        self.uperLeftLocation = l
        self.height = h
        self.width = w

    def intersection(self, point2d, r):
        dup = distance(self.uperLeftLocation.x, self.uperLeftLocation.y, self.uperLeftLocation.x + self.width,
                       self.uperLeftLocation.y, point2d.x, point2d.y)
        dleft = distance(self.uperLeftLocation.x, self.uperLeftLocation.y, self.uperLeftLocation.x,
                         self.uperLeftLocation.y + self.height, point2d.x, point2d.y)
        dright = distance(self.uperLeftLocation.x + self.width, self.uperLeftLocation.y,
                          self.uperLeftLocation.x + self.width, self.uperLeftLocation.y + self.height, point2d.x,
                          point2d.y)
        dbottom = distance(self.uperLeftLocation.x + self.width, self.uperLeftLocation.y ,
                           self.uperLeftLocation.x + self.width, self.uperLeftLocation.y + self.height, point2d.x,
                           point2d.y)

        dmin = min(dup, dleft, dbottom, dright)

        if dmin < r:
            return True
        return False

    def inside(self,point2d):
        if point2d.x>self.uperLeftLocation.x and point2d.x<self.uperLeftLocation.x+self.width and point2d.y > self.uperLeftLocation.y and point2d.y < self.uperLeftLocation.y+self.height :
            return True
        return False


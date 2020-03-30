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
        dup,vu = distance(self.uperLeftLocation.x, self.uperLeftLocation.y, self.uperLeftLocation.x + self.width,
                       self.uperLeftLocation.y, point2d.x, point2d.y)

        dleft,vl = distance(self.uperLeftLocation.x, self.uperLeftLocation.y, self.uperLeftLocation.x,
                         self.uperLeftLocation.y + self.height, point2d.x, point2d.y)
        dright,vr = distance(self.uperLeftLocation.x + self.width, self.uperLeftLocation.y,
                          self.uperLeftLocation.x + self.width, self.uperLeftLocation.y + self.height, point2d.x,
                          point2d.y)
        dbottom,vb = distance(self.uperLeftLocation.x + self.width, self.uperLeftLocation.y ,
                           self.uperLeftLocation.x + self.width, self.uperLeftLocation.y + self.height, point2d.x,
                           point2d.y)

        dmin = min(dup, dleft, dbottom, dright)
        h=None
        if dmin == dup:
            h=vu
        if dmin == dleft:
            h=vl
        if dmin == dright:
            h=vr
        if dmin == dbottom:
            h=vb

        if dmin < r:
            return True,h
        return False,Vector2D(0,0)

    def inside(self,point2d):
        if point2d.x>self.uperLeftLocation.x and point2d.x<self.uperLeftLocation.x+self.width and point2d.y > self.uperLeftLocation.y and point2d.y < self.uperLeftLocation.y+self.height :
            return True
        return False


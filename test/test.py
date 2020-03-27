from math import sqrt


def pointRectDist (px, py, b):

    cx = max(min(px, b.location.x+b.width ), b.location.x)
    cy = max(min(py, b.location.y+b.height),  b.location.y)
    return sqrt( (px-cx)*(px-cx) + (py-cy)*(py-cy) )

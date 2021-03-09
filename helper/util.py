import random
import string

from shapely.geometry import LineString, Point

from helper.vector2D import Vector2D


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def randomInt(m):
    return int(random.uniform(0, m))

def randomRangeInt(n,m):
    return int(random.uniform(n, m))

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def getNextByDistance(source, destinations):
    v = Vector2D(0, 0)
    mini = 100000000
    for d in destinations:
        if source.distance(d.body.location) < mini:
            mini = source.distance(d.body.location)
            v = d
    return v.body


def signedAngle(v1, v2):
    a = Vector2D(v1.x, v1.y)
    if a.getLength() == 0:
        return None

    b = Vector2D(v2.x, v2.y)
    if b.getLength() == 0:
        return None

    a = a.getNormalized()
    b = b.getNormalized()

    cos = a.x * b.x + a.y * b.y;
    sin = a.x * b.y - a.y * b.x;
    angle = math.atan2(sin, cos);
    return angle;


def toOrientationVector(angle):
    return Vector2D(math.cos(angle), math.sin(angle));


# -*- coding: utf-8 -*-

import math


def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    aV=[a.x,a.y]
    bV=[b.x,b.y]
    return sum(i * j for i, j in zip(aV, bV))


def angle_between(a, b):

    angle = math.degrees(math.acos(dot(a, b) / (a.getLength() * b.getLength())))
    return angle


def limit_magnitude(vector, max_magnitude, min_magnitude=0.0):
    mag = magnitude(*vector)
    if mag == 0 :
        return Vector2D()
    if mag > max_magnitude:
        normalizing_factor = max_magnitude / mag
    elif mag < min_magnitude:
        normalizing_factor = min_magnitude / mag
    else:
        return vector

    return [value * normalizing_factor for value in vector]


def rotate_point(x: float, y: float, cx: float, cy: float,
                 angle: float):
    temp_x = x - cx
    temp_y = y - cy

    # now apply rotation
    rotated_x = temp_x * math.cos(math.radians(angle)) - temp_y * math.sin(math.radians(angle))
    rotated_y = temp_x * math.sin(math.radians(angle)) + temp_y * math.cos(math.radians(angle))

    # translate back
    rounding_precision = 2
    x = round(rotated_x + cx, rounding_precision)
    y = round(rotated_y + cy, rounding_precision)

    return x, y


def getIntersectionPoint(center,r, origin, dest):
    p = Point(center.x,center.y)
    c = p.buffer(r).boundary
    l = LineString([(origin.x, origin.y), (dest.x, dest.y)])
    i = c.intersection(l)




def distance(xB, yB, xE, yE, xM, yM):
    a = xE - xB
    b = yE - yB
    w1 = -a * xB - b * yB
    w2 = -a * xE - b * yE
    w3 = a * yB - b * xB

    PMD1 = a * xM + b * yM + w1

    PMD2 = a * xM + b * yM + w2

    PBD2 = a * xB + b * yB + w2

    PED1 = a * xE + b * yE + w1

    if PMD1 * PED1 < 0:
        return math.sqrt((xM - xB) * (xM - xB) + (yM - yB) * (yM - yB)), Vector2D(xB,yB)  # pas de quotient
    if PMD2 * PBD2 < 0:
        return math.sqrt((xM - xE) * (xM - xE) + (yM - yE) * (yM - yE)) , Vector2D(xE,yE) # idem
    if math.sqrt(a * a + b * b) == 0:
        return 99990, Vector2D

    x = abs(b * xM - a * yM + w3)
    y = math.sqrt(a * a + b * b)

    v = Vector2D(a,b)
    d = Vector2D(xM-xB, yM-yB)
    angle = angle_between(d,v)
    norme = d.getLength() * math.cos(math.radians(angle))
    v=v.getNormalized()
    v=v.scale(norme)
    h = Vector2D(xB+v.x,yB+v.y)
    return abs(b * xM - a * yM + w3) / math.sqrt(a * a + b * b), h


def get_four_byte_color(color):
    if len(color) == 4:
        return color
    elif len(color) == 3:
        return color[0], color[1], color[2], 255
    else:
        raise ValueError("This isn't a 3 or 4 byte color")

def inspectAgents(c):
    l = all_subclasses(c)
    n=[]
    for i in l:
        print(i.__name__)
        n.append(i)
    return n

def inspectAgentsDict(c):
    n = {}
    l = all_subclasses(c)
    n[c.__name__]=c
    for i in l:
        n[i.__name__]=i


    return n

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])
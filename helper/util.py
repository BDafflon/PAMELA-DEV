import random
import string

from helper.vector2D import Vector2D


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def randomInt(m):
    return int(random.uniform(0, m))


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
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    angle = math.degrees(math.acos(dot(a, b) / (magnitude(*a) * magnitude(*b))))
    return angle


def limit_magnitude(vector, max_magnitude, min_magnitude=0.0):

    mag = magnitude(*vector)
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

def get_four_byte_color(color) :
    """
    Given a RGB list, it will return RGBA.
    Given a RGBA list, it will return the same RGBA.

    :param Color color: Three or four byte tuple

    :returns:  return: Four byte RGBA tuple
    """

    if len(color) == 4:
        return color
    elif len(color) == 3:
        return color[0], color[1], color[2], 255
    else:
        raise ValueError("This isn't a 3 or 4 byte color")
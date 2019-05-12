import math
from ..types.grid import Point

def slope(a, b):
    return (b.y - a.y) / (b.x - a.x)


def rotate(self, origin, point, angle):
    rads = math.radians(-angle) 
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(rads) * (px - ox) - math.sin(rads) * (py - oy)
    qy = oy + math.sin(rads) * (px - ox) + math.cos(rads) * (py - oy)
    return Point(round(qx), round(qy))
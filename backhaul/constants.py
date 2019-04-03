from enum import Enum
from .types.grid import Point

class GridDirections(Enum):
	FORWARD = Point(1, 0, 0)
	RIGHT = Point(0, -1, 0)
	BACKWARD = Point(-1, 0, 0)
	LEFT = Point(0, 1, 0)
	UP = Point(0, 0, 1)
	DOWN = Point(0, 0, -1)

class CardinalDirection(Enum):
	NORTH = Point(1, 0, 0)
	SOUTH = Point(-1, 0, 0)
	EAST = Point(0, -1, 0)
	WEST = Point(0, 1, 0)

class SpriteFrames(Enum):
	TOP = 'top'
	LEFT = 'left'
	RIGHT = 'right'
	LEFTRIGHT = 'leftright'
	TOPLEFT = 'topleft'
	TOPRIGHT = 'topright'
	FULL = 'full'

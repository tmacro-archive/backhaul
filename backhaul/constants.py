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

class UIScenes(Enum):
	MAINMENU = 'MAIN'
	NEWGAME = 'NEW'
	LOADING = 'LOAD'
	GAMEHUD = 'GAME'

# Tuple indicates in which direction sprites have been "packed"
# These require a offset anchor
class TileAnchors(Enum):
	TOP = (False, False)
	LEFT = (False, True)
	RIGHT =(True, True)
	LEFTRIGHT = (False, True)
	TOPLEFT = (False, False)
	TOPRIGHT = (False, False)
	FULL = (False, False)
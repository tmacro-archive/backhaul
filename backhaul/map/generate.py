import backhaul.map.terrain as terrain
from ..types.grid import Point
from ..constants import CardinalDirection
from ..util.iter import iter_cube
from ..util.log import Log
import json

_log = Log('map.generate')

def fill_cube(map, size, _terrain, center=None):
	# _log.debug("Filling cube %s -> %s with %s"%(topleft, size + topleft, terrain))
	# if _terrain == terrain.id.STONE:
	# 	import ipdb 
	# 	ipdb.set_trace()
	for point in iter_cube(size, center):
		# print(point)
		map.set(point, _terrain)


def generate_base(map):
	start_x = -map.size.x // 2
	start_y = -map.size.y // 2
	start_z = -map.size.z // 2
	start = Point(start_x, start_y, start_z)
	fill_cube(map, map.size, terrain.id.AIR, center=Point(0,0,0))

	fill_cube(map, Point(101, 101, 1), terrain.id.GRASS, center=Point(0, 0, 0))
	# fill_cube(map, Point(15, 15, 1), terrain.id.GRASS, center=Point(0, 0, 0))
	# fill_cube(map, Point(5, 5, 1), terrain.id.STONE, center=Point(0, 0, 1))

	# with open('logo.json') as f:
	# 	logo = json.load(f)

	# from PIL import Image
	# im = Image.open('backhaulsimple.bmp')

	# pixels = im.load() # this is not a list, nor is it list()'able
	# width, height = im.size

	# for x in range(width):
	# 	for y in range(height):
	# 		pixel = pixels[x, y]
	# 		if pixel == (255,255,255):
	# 			map.set(Point(x,y,1), terrain.id.STONE)
	# 			map.set(Point(x,y,2), terrain.id.DIRT)
	# 			map.set(Point(x,y,3), terrain.id.DIRT)
	# 			map.set(Point(x,y,4), terrain.id.DIRT)
	# 			map.set(Point(x,y,5), terrain.id.GRASS)
	# for y in range(-6, 6):
	# 	for x in range(-36,36):
	# 		if not logo[y][x]:
				


	# for x in [-5, +5]:
	# 	map.set(Point(x, 0, 0), terrain.id.STONE)

	# map.set(Point(0, 0, 1), terrain.id.DIRT)
	# map.set(Point(-2, 2, 1), terrain.id.DIRT)
	# map.set(Point(-2, 3, 0), terrain.id.DIRT)
	# map.set(Point(-3, 2, 0), terrain.id.DIRT)
	# map.set(Point(-2, 2, 1), terrain.id.AIR)
	

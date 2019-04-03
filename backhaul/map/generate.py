import backhaul.map.terrain as terrain
from ..types.grid import Point
from ..constants import CardinalDirection
from ..util.iter import iter_cube
from ..util.log import Log

_log = Log('map.generate')

def fill_cube(map, size, terrain, topleft=None):
	_log.debug("Filling cube %s -> %s with %s"%(topleft, size + topleft, terrain))
	for point in iter_cube(size, topleft):
		# print(point)
		map.set(point, terrain)


def generate_base(map):
	start_x = -map.size.x // 2
	start_y = -map.size.y // 2
	start_z = -map.size.z // 2
	start = Point(start_x, start_y, start_z)
	fill_cube(map, map.size, terrain.id.AIR, topleft=start)

	fill_cube(map, Point(30, 30, 1), terrain.id.DIRT, topleft=Point(-15, -15, 0))
	fill_cube(map, Point(14, 14, 1), terrain.id.GRASS, topleft=Point(-7, -7, 0))
	fill_cube(map, Point(3, 3, 1), terrain.id.STONE, topleft=Point(-1, -1, 1))


	# for x in range(-25, 25):
	# 	for y in range(-25, 25):
	# 		print(x, y)
	# 		map.set(Point(x,y,0), terrain.id.DIRT)

	# for x in range(-15, 15):
	# 	for y in range(-15, 15):
	# 		print(x, y)
	# 		map.set(Point(x,y,1), terrain.id.DIRT)
	# for x in range(-5, 5):
	# 	for y in range(-5, 5):
	# 		print(x, y)
	# 		map.set(Point(x,y,2), terrain.id.DIRT)

	# map.set(Point(1,1,2), terrain.id.AIR)
	# map.set(Point(-1,-1,2), terrain.id.AIR)
	# map.set(Point(-1,1,2), terrain.id.AIR)
	# map.set(Point(1,-1,2), terrain.id.AIR)
	# map.set(Point(0,-1,2), terrain.id.AIR)
	# map.set(Point(0,1,2), terrain.id.AIR)
	# map.set(Point(1,0,2), terrain.id.AIR)
	# map.set(Point(-1,0,2), terrain.id.AIR)

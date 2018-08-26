import backhaul.map.terrain as terrain
from hexc import Hex

def fill_slice(pos, radius, terrain):
	for tile in pos.within(radius):
		tile.set( terrain)


def generate_base(map):
	third = int(map.height / 3)
	sixth =  int(third / 3)

	for h in range(map.height):
		center = Hex(0,0,0,h, parent = map)
		if h < third:
			fill_slice(center, map.radius, terrain.id.STONE)
		elif h >= third and h < third + sixth:
			fill_slice(center, map.radius, terrain.id.DIRT)
		elif h == third + sixth:
			fill_slice(center, map.radius, terrain.id.GRASS)

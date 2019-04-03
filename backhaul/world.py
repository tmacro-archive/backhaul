from .util.conf import config
from .util.log import Log
from .map.generate import generate_base
from .map.storage import MemMap
from .types.grid import Point
import tracemalloc

_log = Log('world')



def BuildTestWorld():
	world = World(radius=30)
	generate_base(world.map)
	return world


class World:
	def __init__(self, height = 128, radius = 1500):
		self._map = MemMap(size=Point(radius, radius, height),
							chunk_radius=Point(100,100,height))
	@property
	def map(self):
		return self._map

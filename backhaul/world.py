from .util.conf import config
from .util.log import Log
from hexc import Stack
from .map.generate import generate_base

_log = Log('world')



def BuildTestWorld():
	world = World()
	generate_base(world.map)
	return world


class World:
	def __init__(self, height = 128, radius = 10):
		self._map = Stack(height = height, radius = radius)

	@property
	def map(self):
		return self._map
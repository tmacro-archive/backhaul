from ..util.conf import create_namespace, recurse_update
from ..types.grid import Point
from ..map.generate import generate_base

class WorldConfig:
	map_size = Point(256, 256, 64)

	@classmethod
	def new(cls):
		class _new(cls):
			pass
		return _new

class World:
	def __init__(self, world_config):
		self._world_config = world_config
		self._world_map = None
		self._minions = None
		self._items = None

	def _build_map(self, seed):
		self._world_map = MemMap(
			size=Point(
				self._world_config.map_size.x // 2,
				self._world_config.map_size.x // 2,
				self._world_config.map_size.z),
			chunk_radius=Point(10,10,self._world_config.map_size.z))
		generate_base(self._world_map)

	def build(self, seed, cb=None):
		self._build_map(seed)
		if cb:
			cb()

	@property
	def map(self):
		return self._world_map

	@property
	def minions(self):
		return self._minions

	@property
	def items(self):
		return self._items

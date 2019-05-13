from ..util.conf import create_namespace, recurse_update
from ..types.grid import Point
from ..map.generate import generate_base
from ..map.storage import TerrainMap

class WorldConfig:
	map_size = Point(256, 256, 64)

	@classmethod
	def new(cls):
		class _new(cls):
			pass
		return _new

class World:
	def __init__(self, datastore, world_config):
		self._datastore = datastore
		self._world_config = world_config
		self._world_map = TerrainMap(world_config.map_size, datastore.layers.terrain)
		self._minions = None
		self._items = None

	def _build_map(self, seed):
		# generate_base(self._world_map)
		pass

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


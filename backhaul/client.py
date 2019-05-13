from .ui import BackhaulUI
from .datastore import BackhaulDatastore
from .constants import UIScenes
from .util.conf import config
from .types.grid import Point


class BackhaulClient:
	def __init__(self, host):
		self._ui = BackhaulUI
		self._ui.set_client(self)
		self._datastore = BackhaulDatastore
		self._world = None

	def run(self):
		resolution = Point(*[int(x) for x in config.graphics.resolution.split('x')])
		self._ui.show(resolution)

	@property
	def world(self):
		return self._world

	def create_game(self, name):
		self._world = self._datastore.create(name)
		return self._world
		
	def load_game(self, name):
		self._world = self._datastore.load(name)
		return self._world

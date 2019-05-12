from .ui import BackhaulUI
from .datastore import BackhaulDatastore
from .constants import UIScenes
from .util.conf import config
from .types.grid import Point


class BackhaulClient:
	def __init__(self, host):
		self._ui = BackhaulUI
		self._datastore = BackhaulDatastore

	def run(self):
		resolution = Point(*[int(x) for x in config.graphics.resolution.split('x')])
		self._ui.show(resolution)


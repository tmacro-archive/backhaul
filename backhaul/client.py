from .ui import BackhaulUI
from .constants import UIScenes
from .util.conf import config
from .types.grid import Point


class BackhaulClient:
	def __init__(self, host):
		self._world = self._build_local_world()
		self._client = self._build_client(host, self._world)
		self._ui = BackhaulUI

	def _build_local_world(self):
		pass

	def _build_client(self, host, world):
		pass

	# def _build_ui(self):
	#     return ui.UI(UIScenes.MAINMENU, UI.LOADED_SCENES)

	def run(self):
		resolution = Point(*[int(x) for x in config.graphics.resolution.split('x')])
		self._ui.show(resolution)


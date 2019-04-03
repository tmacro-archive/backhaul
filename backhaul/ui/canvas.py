import pyglet
from ..types.grid import Point
from .map import MapView
from ..util.log import Log

_log = Log('canvas')

class BaseCanvas(pyglet.window.Window):
	def __init__(self, size = Point(500, 500), fullscreen = False, world=None, **kwargs):
		super().__init__(width=size.x, height=size.y, fullscreen = fullscreen, **kwargs)
		self._world = world
		_log.info('Building map view...')
		self._map = MapView(Point(0,0,0), size)
		self._map.init_buffer(self._world.map)
		_log.info('Done building map view')
	def _on_draw(self):
		self.clear()
		self._map.draw(self._world.map)

	def update(self, *args, **kwargs):
		self._on_draw()

import pyglet
# from lib.controls import Controls, Actions
from collections import namedtuple
# from lib.map import MapSlice
from ..util.conf import config
from ..util.log import Log
from hexc import AbstractHex, Hex
from ..util.error import BackhaulError

_log = Log('ui.view')

class View(namedtuple('View', ['center', 'zoom', 'width', 'height'])):
	__slots__ = ()
	@property
	def start(self):
		return self.x1, self.y1
	@property
	def stop(self):
		return self.x2, self.y2

class ViewPort(pyglet.window.Window):
	def __init__(self, world = None, size = (500, 500), fullscreen = False, **kwargs):
		super().__init__(width=size[0], height=size[1], fullscreen = fullscreen, **kwargs)
		self.world = world
		# if self.world is None:
		# 	raise BackhaulError

		self.viewportWidth, self.viewportHeight = size
		self.tiledWidth = int(self.viewportWidth / config.tileWidth)
		self.tiledHeight = int(self.viewportHeight / config.tileHeight)
		_log.debug('Using tile size %s, %s'%(self.tiledHeight, self.tiledWidth))
		self._center = AbstractHex(0,0)
		self.zoom = 0.5 # zoom in percent 1 = 100%, .5 = 50%
		self._block_cache = None
		self._first_run = True
		# self.controls = Controls()
		# self.push_handlers(self.controls)
		self._debugViewCoords = pyglet.text.Label('0, 0, 0',
                          font_name='Times New Roman',
                          font_size=12,
                          x=5, y=5,
                          anchor_x='left', anchor_y='bottom')

	def on_draw(self):
		self.clear()
		self._draw_terrain(self.world.map)
		# self._draw_flora()
		# self._draw_entities()
		if config.logging.debug:
			self._draw_debug()

	def _draw_debug(self):
		self._debugViewCoords.draw()

	def _init_tile_cache(self):
		largest = self.tiledWidth if self.tiledWidth > self.tiledHeight else self.tiledHeight
		cacheRadi = int(largest / 2) + 2
		self._block_cache = Stack(cacheRadi, 1)
		iterRadi = cacheRadi if cacheRadi <= self.world.map.radius else self.world.map.radius
		# for h in Hex(0,0, parent = self._block_cache).within(iterRadi):
		# 	sprite = pyglet.sprite.Sprite(img = self.world.map.get(h.texture))
		# 	h.set(sprite)

	def _draw_terrain(self, map):
		if self._first_run:
			self._init_tile_cache()
			self._first_run = False
		# iterRadi = self._block_cache.radius if self._block_cache.radius <= self.world.map.radius else self.world.map.radius
		# for h in Hex(0, 0, parent = self._block_cache).within(iterRadi):
		# 	s = h.get()
		# 	if s:
		# 		s.draw()
		# 		break
		

	def _draw_flora(self):
		pass

	def _draw_entities(self):
		pass


	def update(self, dt):
		# if self.controls[Actions.CAMERA_UP]:
		# 	# self.viewportY += 1
		# 	# self.viewportX += 1
		# 	self.viewportX += -1
		# 	self.viewportY +=  1
		# if self.controls[Actions.CAMERA_DOWN]:
		# 	# self.viewportY += -1
		# 	# self.viewportX += -1
		# 	self.viewportX +=  1
		# 	self.viewportY += -1

		# if self.controls[Actions.CAMERA_LEFT]:
		# 	# self.viewportX +=  1
		# 	# self.viewportY += -1
		# 	self.viewportY += -1
		# 	self.viewportX += -1

		# if self.controls[Actions.CAMERA_RIGHT]:
		# 	# self.viewportX += -1
		# 	# self.viewportY +=  1
		# 	self.viewportY += 1
		# 	self.viewportX += 1

		self._debugViewCoords.text = '%i, %i, %i'%(self._center.q, self._center.r, self._center.s)

	@property
	def currentView(self):
		return View((self.viewportX, self.viewportY), self.zoom, self.viewportWidth, self.viewportHeight)

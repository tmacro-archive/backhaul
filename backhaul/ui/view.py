import pyglet
# from lib.controls import Controls, Actions
from collections import namedtuple
# from lib.map import MapSlice
from ..util.conf import config
from ..util.log import Log
from hexc import AbstractHex, Hex, Stack
from ..util.error import BackhaulError
from math import sqrt, floor, ceil
_log = Log('ui.view')

class View(namedtuple('View', ['center', 'zoom', 'width', 'height'])):
	__slots__ = ()
	@property
	def start(self):
		return self.x1, self.y1
	@property
	def stop(self):
		return self.x2, self.y2

Orientation = namedtuple('Orientation', ['f0', 'f1', 'f2', 	'f3'])

class Orientations:
	pointy = Orientation(sqrt(3.0), sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0)
	flat = Orientation(3.0 / 2.0, 0.0, sqrt(3.0) / 2.0, sqrt(3.0))

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
						  x=self.viewportWidth / 2, y=self.viewportHeight/2,
						  anchor_x='left', anchor_y='bottom')

	def on_draw(self):
		self.clear()
		# _log.debug('Drawing terrain')
		self._draw_terrain(self.world.map)
		# self._draw_flora()
		# self._draw_entities()
		if config.logging.debug:
			self._draw_debug()

	def _draw_debug(self):
		self._debugViewCoords.draw()

	def _init_tile_cache(self):
		_log.debug('Building tile cache')
		cacheRadius = ceil((self.tiledHeight / (config.graphics.chunk.radius * 2)) / 2) + 1
		cacheHeight = ceil(self.tiledHeight / 2)
		cacheWidth = ceil(self.tiledHeight / 2)
		self._block_cache = Stack(cacheRadius, 1)
		_log.debug('Using cache radius of %i tiles'%cacheRadius)
		offset_x = self.viewportWidth / 2
		offset_y = self.viewportHeight / 2

		# for h in Hex(0,0, parent = self._block_cache).within(cacheRadius):
		for h in self._block_cache.center().within(cacheRadius):
			# tex = self.world.map.get(h)
			center = h * config.graphics.chunk.radius
			_log.debug('Building chunk centered at %s'%center)
			chunk = TileChunk(center, config.graphics.chunk.radius, offset_x, offset_y)
			chunk.build(self.world.map)
			h.set(chunk)

	def _draw_terrain(self, map):
		if self._first_run:
			self._init_tile_cache()
			self._first_run = False
		for h in Hex(0, 0, parent = self._block_cache).within(self._block_cache.radius):
			s = h.get()
			if s:
				s.draw()
		for h in Hex(0, 0, parent = self._block_cache).within(self._block_cache.radius):
			s = h.get()
			if s:
				s.draw_debug()
				# break


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



class TileChunk:
	def __init__(self, center, radius, offset_x, offset_y):
		self._center = center
		self._radius = radius
		self._tiles = None
		self._batch = None
		self._offset_x = offset_x
		self._offset_y = offset_y
		self._debugtxt = None

	def _build_debug(self):
		ctr = self._center
		x, y = self._hex_to_pixel(ctr)
		self._debugtxt = pyglet.text.Label('%i, %i, %i # %i, %i, # %i, %i'%(ctr.q, ctr.r, ctr.s, x, y, x - self._offset_x, y - self._offset_y),
						  font_name='Times New Roman',
						  font_size=12,
						  x=x, y=y,
						  anchor_x='center', anchor_y='center')

	_size_x = config.tileWidth / 2
	_size_y = config.tileHeight / 32 * 17
	def _hex_to_pixel(self, hex, orien = Orientations.flat):
		x = (orien.f0 * hex.q + orien.f1 * hex.r) * self._size_x;
		y = (orien.f2 * hex.q + orien.f3 * hex.r) * self._size_y;
		return x + self._offset_x, y + self._offset_y

	def build(self, map):
		self._tiles = Stack(self._radius, 1)
		self._batch = pyglet.graphics.Batch()
		for tile in Hex(0, 0, parent = self._tiles).within(self._radius):
			# _log.debug('Building sprite for hex at %s'%(tile + self._center))
			texture = map.get(tile + self._center)
			if texture is not None:
				# _log.debug('No hex found at %s'%(tile + self._center))
				x, y = self._hex_to_pixel(tile + self._center)
				sprite = pyglet.sprite.Sprite(img = texture.texture, batch = self._batch, x = x, y = y)
				tile.set(sprite)

	def update(self, offset, offset_x = 0, offset_y = 0):
		for tile in Hex(0, 0, parent = self._tiles).within(self._radius):
			x, y = self._hex_to_pixel(tile + offset + self._center)
			sprite = tile.get()
			if sprite:
				sprite.x = x
				sprite.y = y

	def draw(self):
		self._batch.draw()

	def draw_debug(self):
		if not self._debugtxt:
			self._build_debug()
		self._debugtxt.draw()

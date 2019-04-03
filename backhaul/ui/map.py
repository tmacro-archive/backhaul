import pyglet
from ..map import terrain
from ..types.grid import Point
from ..constants import GridDirections, SpriteFrames, CardinalDirection
from .component import Component
from ..util.log import Log

_log = Log('ui.map')

class Tile(pyglet.sprite.Sprite):
	def __init__(self, image, position, size, offset, batch=None):
		super().__init__(image, batch=batch)
		self.offset = offset
		self._size = size
		self._real_x = None
		self._real_y = None
		self._set_anchor(image, size)
		self.update_position(position)
		self.update()

	def update_position(self, position):
		self._real_x, self._real_y, _ = position

	def _set_anchor(self, image, tile_size):
		anchor = tile_size // Point(2,2,1)
		image.anchor_x = image.width - anchor.x
		image.anchor_y = image.height - anchor.y


	def update(self, *args, **kwargs):
		return super().update(
			x = self._real_x + self.offset.x,
			y = self._real_y + self.offset.y,
			*args, **kwargs
		)

class Offset:
	def __init__(self, parent):
		self._parent = parent

	@property
	def x(self):
		return self._parent._x_offset

	@property
	def y(self):
		return self._parent._y_offset

DEFAULT_TILE_SIZE = Point(32, 16, 32)
MIN_TILE_SIZE = Point(8, 4)
MIN_ZOOM = 0.25
MAX_ZOOM = 8.0


class MapView(Component):
	def __init__(self, position, size, zoom = 1.0):
		super().__init__(position)
		self._size = size
		self._zoom = 1.0
		self._tile_offset = Point(0,0)
		self._buffer = dict()
		self._batch = None
		self._log = _log.getChild('MapView')
		self._direction = CardinalDirection.NORTH

	@property
	def _tile_size(self):
		return Point(int(DEFAULT_TILE_SIZE.x * self._zoom), int(DEFAULT_TILE_SIZE.y * self._zoom))

	@property
	def _tile_width(self):
		self._tile_size.x

	@property
	def _tile_height(self):
		self._tile_size.y

	@property
	def _buffer_width(self):
		return self._size.x // ( DEFAULT_TILE_SIZE.x // 2 ) + 1

	@property
	def _buffer_height(self):
		return self._size.y // ( DEFAULT_TILE_SIZE.y // 2 ) + 1

	@property
	def _buffer_size(self):
		return Point(self._buffer_width, self._buffer_height)

	@property
	def _x_offset(self):
		return self._tile_offset.x

	@property
	def _y_offset(self):
		return self._tile_offset.y

	@property
	def _offset(self):
		return Offset(self)

	def move(self, offset):
		self._tile_offset = self._tile_offset + offset

	def zoom(self, delta):
		new_zoom = self._zoom + delta
		if new_zoom < MIN_ZOOM:
			new_zoom = MIN_ZOOM
		elif new_zoom > MAX_ZOOM:
			new_zoom = MAX_ZOOM
		self._zoom = new_zoom

	def _get_from_map(self, map, position):
		_position = self._tile_offset + position
		return map.get(_position)


	@property
	def _visible_faces(self):
		if self._direction is CardinalDirection.NORTH:
			return {
				'up': GridDirections.UP,
				'right': CardinalDirection.EAST,
				'left': CardinalDirection.SOUTH,
			}
		elif self._direction is CardinalDirection.SOUTH:
			return {
				'up': GridDirections.UP,
				'left': CardinalDirection.WEST,
				'right': CardinalDirection.NORTH,
			}
		elif self._direction is CardinalDirection.EAST:
			return {
				'up': GridDirections.UP,
				'left': CardinalDirection.SOUTH,
				'right': CardinalDirection.WEST,
			}
		elif self._direction is CardinalDirection.WEST:
			return {
				'up': GridDirections.UP,
				'left': CardinalDirection.NORTH,
				'right': CardinalDirection.EAST,
			}

	def _check_visibility(self, map, point):
		_terrain = self._get_from_map(map, point)
		if not _terrain or _terrain == terrain.id.AIR:
			return False
		for name, direction in self._visible_faces.items():
			tile = self._get_from_map(map, point + direction.value)
			if tile == terrain.id.AIR:
				return True

	def _get_sprite(self, map, position):
		_terrain = self._get_from_map(map, position)
		has_air = {k:self._get_from_map(map, d.value + position) is terrain.id.AIR for k,d in self._visible_faces.items() }
		if all(has_air.values()):
			return _terrain.texture.full
		elif has_air['up']:
			if has_air['left']:
				return _terrain.texture.topleft
			if has_air['right']:
				return _terrain.texture.topright
			return _terrain.texture.top
		elif has_air['left'] and has_air['right']:
			return _terrain.texture.leftright
		elif has_air['left']:
			return _terrain.texture.left
		elif has_air['right']:
			return _terrain.texture.right

	def _project(self, point):
		pt = Point(
			(point.x - point.y) * (self._tile_size.x // 2) + (self._size.x // 2),
			(point.x + point.y) * (self._tile_size.y // 2) + (self._size.y // 2)
		)
		# print ('%s -> %s'%(point, pt))
		return pt

	def _draw_debug_point(self, point):
		center = self._project(point)
		pixels = [center.x, center.y]
		for direction in CardinalDirection:
			offset = direction.value+center
			pixels.append(offset.x)
			pixels.append(offset.y)
		pyglet.graphics.draw(5, pyglet.gl.GL_POINTS,
			('v2i', tuple(pixels)),
			('c3B', (250, 50, 0)*5)
		)

	def init_buffer(self, map):
		self._log.debug('Building buffer...')
		print(self._buffer_size)
		for x in range(-self._buffer_width // 2, self._buffer_width // 2 + 1):
			for y in range(-self._buffer_height // 2, self._buffer_height // 2 + 1):
				for z in range(map.size.z, -1, -1):
					position = Point(x, y, z)
					if self._check_visibility(map, position):
						spr = self._get_sprite(map, position)
						tile_position = self._project(position)
						self._buffer[position] = Tile(spr, tile_position, self._tile_size, self._offset, batch=self.batch)
						break

		# for x in range(-25, 25):
		# 	for y in range(-25, 25):
		# 		for z in range(map.size.z, -1, -1):
		# 			position = Point(x,y,z)
		# 			# if position.x != 0:
		# 			# if position != Point(0,0,0) and position != Point(1,0,0):
		# 			# 	continue

		# 			if self._check_visibility(map, position):
		# 				# self._log.debug('Tile visible adding to buffer')
		# 				spr = self._get_sprite(map, position)
		# 				tile_position = self._project(position)
		# 				# print(tile_position)
		# 				self._buffer[position] = Tile(spr, tile_position, self._tile_size, self._offset, batch=self.batch)

	@property
	def batch(self):
		if self._batch is None:
			self._batch = pyglet.graphics.Batch()
		return self._batch

	def _draw_debug(self):
		for x in range(-1, 2):
			for y in range(-1, 2):
				self._draw_debug_point(Point(x,y))

	def draw(self, map):
		self.batch.draw()
		self._draw_debug()

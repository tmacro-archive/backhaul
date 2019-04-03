import pyglet
import glooey
from ...util.log import Log
from ...util.conf import config
from ...util.iter import iter_cube
from ...types.grid import Point
from ..constants import GridDirections, SpriteFrames, CardinalDirection
from ..map import terrain

_log = Log('ui.components.map')

class Tile(pyglet.sprite.Sprite):
	def __init__(self, image, position, size, **kwargs):
		super().__init__(image, **kwargs)
		anchor = tile_size // Point(2,2,1)
		image.anchor_x = image.width - anchor.x
		image.anchor_y = image.height - anchor.y

class Map(glooey.Widget):
	custom_tile_size = None

	def __init__(self, map):
        super().__init__()
		self.__sprites = None
		self.__buffer = None
		self.__tile_size = Point(*custom_default_tile_size)
		self.__map = map
		self.__has_changed = True

	@property
	def _widget_size(self):
		return Point(*self.get_window().get_size())

	@property
	def _buffer_size(self):
		window_size = self.get_window().get_size()
		half_tile = self.__tile_size // Point(2, 2, 1)
		return Point(*window_size) // half_tile

	@property
	def _buffer(self):
		if self.__buffer is None:
			self.__buffer = self._build_buffer()
		return self.__buffer

	def _build_buffer(self):
		_log.debug('Building buffer of size %s, %s, %s'%)
		buffer = dict()
		for point in iter_cube(self._buffer_size, Point(0,0,0)):
			if self._check_tile_visibility(point):
				texture = self._get_tile_texture(position)
				tile_position = self._iso_project(position)
				buffer[position] = (
					sprite,
					tile_position,
					self.__tile_size,
				)
				break # Only the top visible tile is shown for now

	def _get_from_map(self, map, position):
		_position = self._tile_offset + position
		return self.map.get(_position)

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

	def _check_tile_visibility(self, point):
		_terrain = self._get_from_map(point)
		if not _terrain or _terrain == terrain.id.AIR:
			return False
		for name, direction in self._visible_faces.items():
			tile = self._get_from_map(point + direction.value)
			if tile == terrain.id.AIR:
				return True

	def _get_tile_texture(self, position):
		_terrain = self._get_from_map(position)
		has_air = dict()
		for key, direction in self._visible_faces.items():
			has_air[k] = self._get_from_map(direction.value + \
											position) is terrain.id.AIR
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

	def _iso_project(self, point):
		pt = Point(
			(point.x - point.y) * (self.__tile_size.x // 2) + (self._widget_size.x // 2),
			(point.x + point.y) * (self.__tile_size.y // 2) + (self._widget_size.y // 2)
		)
		# print ('%s -> %s'%(point, pt))
		return pt

	@property
	def _sprites(self):
		if self.__sprites is None:
			self.__sprites = self._build_sprites()
		return self.__sprites

	def _build_sprites(self):
		sprites = dict()
		for pos, tile in self.__buffer.items():
			sprites[pos] = Tile(
				*tile,
				batch=self.get_batch(),
				group=self.get_group()
			)
		return sprites

	# Return space needed by widget
	def do_claim(self):
		return self._widget_size

	# Called when attached to new group
	def do_regroup(self):
		for tile in self._buffer.values():
			tile.group = self.get_group()

	def _draw_debug_point(self, point):
		center = self._iso_project(point)
		pixels = [center.x, center.y]
		for direction in CardinalDirection:
			offset = direction.value+center
			pixels.append(offset.x)
			pixels.append(offset.y)
		pyglet.graphics.draw(5, pyglet.gl.GL_POINTS,
			('v2i', tuple(pixels)),
			('c3B', (250, 50, 0)*5)
		)

	def _draw_debug(self):
		for x in range(-10, 11):
			for y in range(-10, 11):
				self._draw_debug_point(Point(x,y))

	# Draw some shit
	def do_draw(self):
		if self.__has_changed:
			for sprite in self._sprites:
				continue # Do some stuff in the future
			self.__has_changed = False

	# Delete some shit
	def do_undraw(self):
		# Delete the sprites maybe?
		pass

	# Called when attached to GUI
	def do_attach(self):
		pass


	# Called when detached from GUI
    def do_detach(self):
		pass

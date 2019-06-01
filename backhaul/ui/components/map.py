import pyglet
import glooey
from ...util.log import Log
from ...util.conf import config
from ...util.iter import iter_cube, smart_range, center_range
from ...types.grid import Point
from ...constants import GridDirections, SpriteFrames, CardinalDirection
from ...map import terrain
import autoprop
import math

_log = Log('ui.components.map')

class Tile(pyglet.sprite.Sprite):
	def __init__(self, image, position, size, **kwargs):
		super().__init__(image, **kwargs)
		# anchor = size // Point(2,2,1)
		# image.anchor_x = image.width - anchor.x
		# image.anchor_y = image.height - anchor.y
		self.set_position(position)
	
	def set_position(self, position):
		self.position = (position[0], position[1])


class MapContainer(glooey.Stack):
	def __init__(self):
		super().__init__()
		self.alignment = 'fill'
		self.__map = None

	def set_map(self, map):
		self.__map = map

	def get_map(self):
		return self.__map

@autoprop
class Map(glooey.Widget):
	custom_default_tile_size = (16, 8, 8)

	def __init__(self, map = None):
		super().__init__()
		self.__sprites = None
		self.__buffer = None
		self.__tile_size = Point(*self.custom_default_tile_size)
		self._tile_offset = Point(0,0,0)
		self.__map = map
		self.__has_changed = False
		self._direction = CardinalDirection.NORTH

	@property
	def _widget_size(self):
		return Point(*self.get_window().get_size())

	@property
	def _buffer_size(self):
		window_size = self.get_window().get_size()
		half_tile = self.__tile_size // Point(2, 2, 1)
		wh = Point(*window_size) // half_tile
		# return Point(11, 11, 10)
		return Point(wh[0] - 1, wh[1], 10)

	@property
	def _buffer(self):
		if self.__buffer is None:
			self.__buffer = self._build_buffer()
		return self.__buffer

	def _build_buffer(self):
		_log.debug('Building buffer of size %s, %s, %s'%self._buffer_size)
		buffer = dict()
		# for point in iter_cube(self._buffer_size, Point(0,0,0)):
		for point in self._iter_screen():
			# if point == Point(3,-2,0):
			# 	continue
			# if point.z > 0 and point != Point(-2,2,1) and point != Point(2,-2,1) and point != Point(-2,-2,1) and point != Point(2,2,1):
			# 	continue
			if self._check_tile_visibility(point):
				texture = self._get_tile_texture(point)
				tile_position = self._iso_project(point)
				buffer[point] = (
					texture,
					tile_position,
					self.__tile_size,
				)
				# break # Only the top visible tile is shown for now
		_log.debug('Done Building Buffer')
		# print(len(buffer))
		return buffer

	def refresh_buffer(self):
		self.__buffer = self._build_buffer()
		self.__has_changed = True

	# Iterates over the points that will appear on screen
	def _iter_screen(self):
		buffer_size = self._buffer_size
		half_width = buffer_size.x // 4 # convert to full tile widths then center
		half_height = buffer_size.y // 4
		topleft = Point(-half_width, half_width) + Point(half_height, half_height)
		print(topleft)
		print(topleft + (buffer_size // Point(2, 2, 1)))
		# topleft = self.rotate((0,0), topleft[:2], 45)
		# print(topleft)
		for z in smart_range(*center_range(buffer_size.z)):
			for x in range(buffer_size.x // 2):
				for y in range(buffer_size.y // 2):
					yield topleft + Point(-x, -x, 0) + Point(y, -y, z)
				for y in range(buffer_size.y // 2):
					yield topleft + Point(-x-1, -x, 0) + Point(y, -y, z)



	def get_map(self):
		return self.__map

	def set_map(self, value):
		# print(value)
		self.__map = value

	def _get_from_map(self, position):
		if self.map is not None:
			print('fffff')
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
		# if point.x == -3 and point.y == -3 and point.z == 1:
		# 	import ipdb 
		# 	ipdb.set_trace()
		_terrain = self._get_from_map(point)
		print(_terrain)
		if not _terrain or _terrain == terrain.id.AIR:
			return False
		for name, direction in self._visible_faces.items():
			tile = self._get_from_map(point + direction.value)
			print(tile)
			if tile == terrain.id.AIR:
				print(point)
				return True

	def _get_tile_texture(self, position):
		_terrain = self._get_from_map(position)
		has_air = dict()
		for key, direction in self._visible_faces.items():
			has_air[key] = self._get_from_map(direction.value + \
											position) is terrain.id.AIR
		if all(has_air.values()):
			# print(f'Chose FULL texture for {position}')
			return _terrain.texture.full
		elif has_air['up']:
			if has_air['left']:
				# print(f'Chose TOPLEFT texture for {position}')
				return _terrain.texture.topleft
			if has_air['right']:
				# print(f'Chose TOPRIGHT texture for {position}')
				return _terrain.texture.topright
			# print(f'Chose TOP texture for {position}')
			return _terrain.texture.top
		elif has_air['left'] and has_air['right']:
			# print(f'Chose LEFTRIGHT texture for {position}')
			return _terrain.texture.leftright
		elif has_air['left']:
			# print(f'Chose LEFT texture for {position}')
			return _terrain.texture.left
		elif has_air['right']:
			# print(f'Chose RIGHT texture for {position}')
			return _terrain.texture.right

	def _iso_project(self, point):
		pt = Point(
			(point.x - point.y) * (self.__tile_size.x // 2) + (self._widget_size.x // 2),
			(point.x + point.y) * (self.__tile_size.y // 2) + (self._widget_size.y // 2)
		)
		z_height_adjust = point.z * self.__tile_size.y
		final = pt + Point(0, z_height_adjust, 0)
		# print ('%s -> %s'%(point, final))
		return final

	def _screen_to_map(self, point):
		uncentered = point - (self._widget_size // Point(2,2,1))
		return Point(
			math.floor((uncentered.x / (self.__tile_size.x // 2) + self._widget_size.y / (self.__tile_size.y // 2)) / 2),
			math.floor((uncentered.y / (self.__tile_size.y // 2) - (self._widget_size.x / (self.__tile_size.x // 2))) / 2),
			0
		)

	@property
	def _sprites(self):
		if self.__sprites is None:
			self.__sprites = self._build_sprites()
		return self.__sprites

	def _get_tile_group(self, group):
		return pyglet.graphics.OrderedGroup(group, self.get_group())

	def _build_sprites(self):
		sprites = dict()
		for pos, tile in self._buffer.items():
			sprites[pos] = Tile(
				*tile,
				batch=self.get_batch(),
				group=self._get_tile_group(pos.z)
			)
		return sprites

	def refresh_sprites(self):
		if self.__has_changed:
			self.__sprites = self._build_sprites()

	# Return space needed by widget
	def do_claim(self):
		# print(self._widget_size[:2])
		return self._widget_size[:2]

	# Called when attached to new group
	def do_regroup(self):
		if self.__buffer:
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
			_log.debug('Drawing Map')
			self._sprites
			# for sprite in self._sprites:
			# 	continue # Do some stuff in the future
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

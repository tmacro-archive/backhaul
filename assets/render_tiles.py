from pathlib import PosixPath
from math import ceil


from PIL import Image, ImageDraw

OUTPUT_DIR =  PosixPath('.')

TILE_WIDTH = 32
TILE_HEIGHT = 16
TILE_WIDTH_HALF = TILE_WIDTH // 2
TILE_HEIGHT_HALF = TILE_HEIGHT // 2


def project_point(x, y):
	return (x - y) * 2.0, (x + y) * 1.0

def center(x, y):
	return x + TILE_WIDTH_HALF, y + TILE_HEIGHT_HALF

def project(x, y):
	return center(*project_point(x, y))

def as_list(f):
	def inner(*args, **kwargs):
		return list(f(*args, **kwargs))
	return inner

@as_list
def plane(w, h):
	yield project(-w, h)
	yield project(w, h)
	yield project(w, -h)
	yield project(-w, -h)

def _tpoint(x, y, p):
	return p[0] + x, p[1] + y

@as_list
def translate(x, y, points):
	for start, stop in points:
		yield (start[0] + x, start[1] + y), (stop[0] + x, stop[1] + y)

@as_list
def extrude(x, y, edge):
	start, stop = edge
	yield start, stop
	yield start, _tpoint(x, y, start)
	yield stop, _tpoint(x, y, stop)
	yield _tpoint(x, y, start), _tpoint(x, y, stop)





def bresenham(a, b):
	"""Yield integer coordinates on the line from (x0, y0) to (x1, y1).
	Input coordinates should be integers.
	The result will contain both the start and the end point.
	"""
	x0, y0 = a
	x1, y1 = b
	dx = x1 - x0
	dy = y1 - y0

	xsign = 1 if dx > 0 else -1
	ysign = 1 if dy > 0 else -1

	dx = abs(dx)
	dy = abs(dy)

	if dx > dy:
		xx, xy, yx, yy = xsign, 0, 0, ysign
	else:
		dx, dy = dy, dx
		xx, xy, yx, yy = 0, ysign, xsign, 0

	D = 2*dy - dx
	y = 0

	for x in range(dx + 1):
		yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
		if D >= 0:
			y += 1
			D -= 2*dx
		D += 2*dy



def color(r=0, g=0, b=0, a=255):
	return r, g, b, a

# Takes list of points [(1,1),(2,1), (3,2)]
# yields edges -> ((1,1),(2,1)), ((2,1),(3,2))

# def plane_to_lines(plane):
# 	for i in range(len(plane)-1):
# 		yield plane[i], plane[i+1]
# 	yield plane[0], plane[-1]


class Canvas:
	def __init__(self, size, scale, offset=(0,0)):
		self._size = size
		self._scale = scale
		self._img = None
		self._offset = offset

	@property
	def size(self):
		return self._size

	def _scale_point(self, point):
		return int(point[0] * self._scale), int(point[1] * self._scale)

	@property
	def scaled(self):
		return self._scale_point(self._size)

	@property
	def width(self):
		return self._size[0]

	@property
	def height(self):
		return self._size[1]

	@property
	def img(self):
		if self._img is None:
			self._img = Image.new(mode='RGBA', size=self.scaled, color=color(a=0))
		return self._img

	def _draw_pix(self, point, color):
		scaled = self._scale_point(point)
		pix = self.img.load()
		for i in range(int(self._scale)):
			for o  in range(int(self._scale)):
				_point = scaled[0] + i, scaled[1] + o
				_point = _point[0] + self._offset[0], _point[1] + self._offset[1]
				pix[_point] = color

	def set(self, point, color):
		self._draw_pix(point, color)

	def save(self, name):
		self.img.save(name)



class Sprite:
	def __init__(self, h, offset, color, outline):
		self._w = h * 2
		self._h = h
		self._color = color
		self._outline = outline
		self._offset = offset
		self._calc_edges(self._w, self._h, offset)
		self._border_map = None

	def _calc_edges(self, w, h, offset):
		wo, ho = offset
		wh = w // 2
		hh = h // 2
		hht=hh-1
		hhb=hh
		whl=wh-1
		whr=wh
		self._tl = ( ( wo, ho + hht ), ( wo + whl, ho ) )
		self._tr = ( ( wo + whr, ho ), ( wo + w - 1, ho + hht ) )
		self._br = ( ( wo + w - 1, ho + hhb ), ( wo + whr, ho + h - 1 ) )
		self._bl = ( ( wo + whl,  ho + h - 1 ), ( wo, ho + hhb ) )

	def _calc_border_map(self, plane):
		bm = [[None]*(self._h*2) for x in range(self._w)]
		for line in plane:
			# print(line)
			for x, y in bresenham(*line):
				# print(x, y)
				bm[x][y] = True
		return bm

	def _dline(self, a, b, img):
		for point in bresenham(a, b):
			img.set(point, self._outline)

	def _dplane(self, plane, img):
		for start, stop in plane:
			self._dline(start, stop, img)

	def _within_bm(self, bm, point):
		x, y  = point
		if bm[x][y]:
			return True
		return True in bm[x][:y] and True in bm[x][y:]

	def _fplane(self, plane, img):
		bm = self._calc_border_map(plane)
		for x in range(self._w):
			for y in range(self._h*2):
				if self._within_bm(bm, (x, y)):
					# print(x, y)
					img.set((x,y), self._color)
		self._dplane(plane, img)


	def top(self):
		return [
			self._tl,
			self._tr,
			self._bl,
			self._br
		]

	def bottom(self, tr=True):
		if tr:
			return translate(0, self._h, self.top())
		return self.top()

	def left(self, ex=True):
		return extrude(0, self._h, self._bl)

	def right(self, ex=True):
		return extrude(0, self._h, self._br)

	def draw(self, img, top=False, left=False, right=False):
		# self._fplane(self.bottom, img)
		if top:
			print('top')
			self._fplane(self.top(), img)
		if left:
			print('left')
			# print(self.top())
			# print(self.left())
			self._fplane(self.left(), img)
		if right:
			print('right')
			# print(self.right())
			self._fplane(self.right(), img)




if __name__ == '__main__':
	width = TILE_WIDTH
	height = TILE_HEIGHT

	black = color()
	clear = color(a=0)
	# green = color(96, 151, 50)
	green = color(95, 255, 88)
	dark_green = color(62, 165, 57)
	brown = color(255, 148, 92)
	dark_brown = color(150, 87, 54)
	grey = color(191, 191, 191)
	dark_grey = color(91, 91, 91)

	# green = color(96, 151, 50, 128)

	# image = Image.new(mode='RGBA', size=(width, height), color=clear)

	# pix = image.load()
	# top = [
	# 	(0,32),
	# 	(64,0),
	# 	(65,0),
	# 	(128,32),
	# 	(128,33),
	# 	(65,64),
	# 	(64,64),
	# 	(0,33)
	# ]

	# draw_line((0,31), (63,0), pix, green)
	# draw_line((64,0), (127,31), pix, green)
	# draw_line((127,32), (64,63), pix, green)
	# draw_line((63,63), (0,32), pix, green)
	frames = {
		'top': ({ 'top' : True }, (1, 1), (0,0)),
		'left': ({ 'left' : True }, (0.5, 1.5), (0, -0.5)),
		'right': ({ 'right' : True }, (0.5, 1.5), (-0.5, -0.5)),
		'topleft': ({ 'top' : True, 'left' : True }, (1, 2), (0,0)),
		'topright': ({ 'top' : True, 'right' : True }, (1, 2), (0,0)),
		'leftright': ({ 'left': True, 'right': True }, (1, 1.5), (0,-0.5)),
		'full': ({ 'top' : True, 'left' : True, 'right' : True }, (1, 2), (0,0))
	}


	tiles = {
		'grass': (green, dark_green),
		'dirt': (brown, dark_brown),
		'stone': (grey, dark_grey)
	}

	for tile, colors in tiles.items():
		s = Sprite(TILE_HEIGHT, (0, 0), *colors)
		for name, frame in frames.items():
			sides, size, offset = frame
			c_width = ceil( width * size[0] )
			c_height = ceil( height * size[1] )
			c_offset_x = ceil( width * offset[0] )
			c_offset_y = ceil( height * offset[1])
			image = Canvas((c_width, c_height), 1, (c_offset_x, c_offset_y))
			s.draw(image, **sides)
			image.save(f'{tile}-{name}.png')




	# s2 = Sprite(TILE_HEIGHT, (0, TILE_HEIGHT), green)
	# s3 = Sprite(TILE_HEIGHT, (0, TILE_HEIGHT*2), green)
	# s4 = Sprite(TILE_HEIGHT, (0, TILE_HEIGHT*3), green)
	# s5 = Sprite(TILE_HEIGHT, (TILE_WIDTH_HALF, int(TILE_HEIGHT*1.5)), green)
	# s6 = Sprite(TILE_HEIGHT, (TILE_WIDTH_HALF, int(TILE_HEIGHT*2.5)), green)
	# s4.draw(image)
	# s5.draw(image)
	# s3.draw(image)
	# s6.draw(image)
	# s2.draw(image)
	# s1.draw(image)





	# draw.polygon(xy=top, fill=green, outline=outline)

	# draw.line(top, fill=255, width=1)
	# draw.line(bottom, fill=255, width=1)
	# draw.line(left, fill=255, width=1)
	# draw.line(right, fill=255, width=1)
	# del draw

	# image.show()

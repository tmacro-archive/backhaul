from .image import Canvas
from .draw import bresenham, translate, extrude
from math import ceil
from pathlib import PosixPath

class Tile:
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

	def _doutline(self, plane, img):
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

	def _draw_plane(self, plane, img, outline=True):
		self._fplane(plane, img)
		if outline:
			self._doutline(plane, img)

	def draw(self, img, top=False, left=False, right=False, outline=True):
		if top:
			self._draw_plane(self.top(), img, outline)
		if left:
			self._draw_plane(self.left(), img, outline)
		if right:
			self._draw_plane(self.right(), img, outline)

TILE_FRAMES = {
	'top': ({ 'top' : True }, (1, 1), (0,0)),
	'left': ({ 'left' : True }, (0.5, 1.5), (0, -0.5)),
	'right': ({ 'right' : True }, (0.5, 1.5), (-0.5, -0.5)),
	'topleft': ({ 'top' : True, 'left' : True }, (1, 2), (0,0)),
	'topright': ({ 'top' : True, 'right' : True }, (1, 2), (0,0)),
	'leftright': ({ 'left': True, 'right': True }, (1, 1.5), (0,-0.5)),
	'full': ({ 'top' : True, 'left' : True, 'right' : True }, (1, 2), (0,0))
}


def draw_tile(name, color, height, scale, output, outline=None):
	width = height * 2
	s = Tile(height, (0,0), color.rgba, outline=outline)
	for frame_name, frame in TILE_FRAMES.items():
		sides, size, offset = frame
		c_width = ceil( width * size[0] )
		c_height = ceil( height * size[1] )
		c_offset_x = ceil( width * offset[0] )
		c_offset_y = ceil( height * offset[1])

		image = Canvas((c_width, c_height), scale, (c_offset_x, c_offset_y))
		s.draw(image, **sides)
		image_path = output / PosixPath(f'{name}-{frame_name}.png')
		image.save(image_path)

from PIL import Image, ImageDraw

class Color:
	def __init__(self, hex, alpha=255):
		rgb = self._hex_to_rgb(hex)
		self._color = (*rgb, alpha)

	def _hex_to_rgb(self, hex):
		h = hex.lstrip('#')
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

	@property
	def rgb(self):
		return tuple(self._color[:3])

	@property
	def rgba(self):
		return self._color

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
			self._img = Image.new(mode='RGBA', size=self.scaled, color=(0,0,0,0))
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

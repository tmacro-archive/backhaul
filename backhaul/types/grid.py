from collections import namedtuple
from functools import partialmethod
from math import floor

class Point(namedtuple('Point', 'x y z', defaults=[0])):
	__slots__ = ()
	def __add__(self, other):
		return self._make((
			self.x + other.x,
			self.y + other.y,
			self.z + other.z
		))
	def __sub__(self, other):
		return self._make((
			self.x - other.x,
			self.y - other.y,
			self.z - other.z
		))
	def __mul__(self, other):
		return self._make((
			floor(self.x * other.x),
			floor(self.y * other.y),
			floor(self.z * other.z)
		))
	def __floordiv__(self, other):
		return self._make((
			floor(self.x / other.x),
			floor(self.y / other.y),
			floor(self.z / other.z)
		))


def add_point(a, b, cls=tuple):
	return cls((
		a.x + b.x,
		a.y + b.y,
		a.z + b.z if a.z is not None and b.z is not None else None
	))
def subtr_point(a, b, cls=tuple):
	return cls((
		a.x - b.x,
		a.y - b.y,
		a.z - b.z if a.z is not None and b.z is not None else None
	))
def multp_point(a, b, cls=tuple):
	return cls((
		a.x * b.x,
		a.y * b.y,
		a.z * b.z if a.z is not None and b.z is not None else None
	))

def div_point(a, b, cls=tuple):
	return cls((
		a.x // b.x,
		a.y // b.y,
		a.z // b.z if a.z is not None and b.z is not None else None
	))

# class Coord:
# 	def __init__(self, x, y, z=None):
# 		self.x = x
# 		self.y = y
# 		self.z = z

# 	__add__ = partialmethod(add_point, cls=Coord)
# 	__sub__ = partialmethod(subtr_point, cls=Coord)
# 	__mul__ = partialmethod(multp_point, cls=Coord)
# 	__floordiv__ = partialmethod(div_point, cls=Coord)

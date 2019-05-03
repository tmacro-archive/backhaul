from ..types.grid import Point

# from collections import namedtuple
# from functools import partialmethod
# from math import floor

# class Point(namedtuple('Point', 'x y z', defaults=[0])):
# 	__slots__ = ()
# 	def __add__(self, other):
# 		return self._make((
# 			self.x + other.x,
# 			self.y + other.y,
# 			self.z + other.z
# 		))
# 	def __sub__(self, other):
# 		return self._make((
# 			self.x - other.x,
# 			self.y - other.y,
# 			self.z - other.z
# 		))
# 	def __mul__(self, other):
# 		return self._make((
# 			floor(self.x * other.x),
# 			floor(self.y * other.y),
# 			floor(self.z * other.z)
# 		))
# 	def __floordiv__(self, other):
# 		return self._make((
# 			floor(self.x / other.x),
# 			floor(self.y / other.y),
# 			floor(self.z / other.z)
#		))

def smart_range(start, stop, reverse=False):
	'''Correctly handles iterating over ranges in 
	either direction including negative numbers'''
	direction = 1 if stop > start else -1
	diff = abs(start - stop) if start > stop else abs(stop - start)
	if reverse:
		direction *= -1 # Reverse our iteration direction
		start = stop + direction # Shift by 1 to maintain start/end
	for x in range(diff):
		yield int(x * direction + start)

def center_range(length, center=0):
	if length == 0:
		return 0, 0
	if length == 1:
		return center, center + 1
	half = length  // 2
	return half * -1 + center, half * -1 + length + center

def iter_cube(size, center=None):
	for x in smart_range(*center_range(size.x, center.x)):
		for y in smart_range(*center_range(size.y, center.y)):
			for z in smart_range(*center_range(size.z, center.z)): # Do this because we want to iter top down
				yield Point(x, y, z)


def iter_slice(size, center):
	half = size // Point(2,2,1)
	start = half * Point(-1,-1,1) + center
	end  = half + center
	for x in range(start.x, end.x):
		for y in range(start.y, end.y):
			yield Point(x, y, center.z)


def test_cube():
	for p in iter_cube(Point(5,5,1), Point(0,0,1)):
		print(p)


# test_cube()
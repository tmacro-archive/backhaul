from ..types.grid import Point


def iter_cube(size, center):
	half = size // Point(2, 2, 2)
	start = half * Point(-1, -1, -1) + center
	end  = half + center
	for x in range(start.x, end.x):
		for y in range(start.y, end.y):
			for z in range(end.z - 1, start.z - 1, -1): # Do this because we want to iter top down
				yield Point(x, y, z)




def iter_slice(size, center):
	half = size // Point(2,2,1)
	start = half * Point(-1,-1,1) + center
	end  = half + center
	for x in range(start.x, end.x):
		for y in range(start.y, end.y):
			yield Point(x, y, center.z)

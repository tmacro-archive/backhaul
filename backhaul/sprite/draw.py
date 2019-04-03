

def as_list(f):
	def inner(*args, **kwargs):
		return list(f(*args, **kwargs))
	return inner

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

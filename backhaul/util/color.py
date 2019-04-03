


def hex_to_rgb(hex):
	h = hex.lstrip('#')
	return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

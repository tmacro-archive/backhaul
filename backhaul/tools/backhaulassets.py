from ..util.arg import option, flag
from pathlib import PosixPath
from ..sprite.image import Color


def register_args():
	@flag('-v', '--verbose', dest='logging.loglvl')
	def verbose(*args, **kwargs):
		return 'debug'

	@option('-p', '--primary', dest='runtime.primary', metavar='PRIMARY', required=True)
	def primary(value):
		return Color(value)

	@option('-s', '--secondary', dest='runtime.secondary', metavar='SECONDARY', default=None)
	def secondary(value):
		return Color(value)

	# @option('--scale', dest='runtime.scale', metavar='SCALE')
	# def scale(value):
	# 	return int(value)

	@option('-z', '--height', dest='runtime.height', metavar='SIZE', required=True)
	def tile_size(value):
		return int(value)

	@option('-n', '--name', dest='runtime.name', metavar='NAME', required=True)
	def name(value):
		return value


	@option('-o', '--outut-path', dest='runtime.outut', metavar='OUTPUT')
	def output(value):
		return PosixPath(value)

def main():
	register_args()
	from ..util.conf import config
	from ..sprite.tile import draw_tile
	from ..sprite.image import Color
	tile_path = config.assets.tiles.resolve()
	draw_tile(config.runtime.name, config.runtime.primary, config.runtime.height, 1, tile_path, outline=config.runtime.secondary.rgba)

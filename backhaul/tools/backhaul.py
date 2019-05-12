from ..util.arg import option, flag

def register_args():
	@flag('-v', '--verbose', dest='logging.loglvl')
	def verbose(*args, **kwargs):
		return 'debug'

def main():
	register_args()
	from ..util.log import setupLogging, Log
	from ..util.conf import config

	setupLogging(config.meta.name, config.meta.version, **config.logging._asdict())

	import pyglet
	from ..types.grid import Point
	from ..client import BackhaulClient

	_log = Log('cli')

	_log.debug('Creating Backhaul client...')
	game_client = BackhaulClient('localhost')
	_log.debug('Done, Starting Backhaul.')
	game_client.run()
	pyglet.app.run()

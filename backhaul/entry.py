import pyglet
from .util.conf import config
from .util.log import Log
from .types.grid import Point
from .client import BackhaulClient

_log = Log('entry.entrypoint')

def entrypoint():
	_log.debug('Creating Backhaul client...')
	game_client = BackhaulClient('localhost')
	_log.debug('Done, Starting Backhaul.')
	game_client.run()
	pyglet.app.run()

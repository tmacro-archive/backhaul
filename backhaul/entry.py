import pyglet
from .util.conf import config
from .util.log import Log
from .ui import ViewPort
from .world import BuildTestWorld

_log = Log('entry.entrypoint')

def entrypoint():
	_log.debug('Building Test World...')
	world = BuildTestWorld()
	_log.debug('Done!\n Starting Game...')
	# world = True
	resolution = [int(x) for x in config.graphics.resolution.split('x')]
	vp = ViewPort(world = world, size = resolution, fullscreen = config.graphics.fullscreen)

	pyglet.clock.schedule_interval(vp.update, 1/60.0)

	pyglet.app.run()

import pyglet
from .util.conf import config
from .util.log import Log
# from .ui import BaseCanvas
# from .world import BuildTestWorld
from .types.grid import Point
# import tracemalloc
from .ui import BackhaulUI

_log = Log('entry.entrypoint')

def entrypoint():
	# _log.debug('Building Test World...')
	# world = BuildTestWorld()
	# _log.debug('Done!\n Starting Game...')
	# # world = True
	resolution = Point(*[int(x) for x in config.graphics.resolution.split('x')])
	# vp = BaseCanvas(size = resolution, fullscreen = config.graphics.fullscreen, world=world)

	# pyglet.clock.schedule_interval(vp.update, 1/60.0)
	BackhaulUI.show(resolution, False)
	# ui.init()
	pyglet.app.run()

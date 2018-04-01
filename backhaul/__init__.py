import pyglet
from .util.conf import config
from .util.log import Log

_log = Log('backhaul')


assets = getattr(config, 'assets', None)
if assets is not None:
    _log.debug('Initializing resource paths')
    pyglet.resource.path = assets[:]
    pyglet.resource.reindex()
else:
    _log.warning('No asset paths defined!')


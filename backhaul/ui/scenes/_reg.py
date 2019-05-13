from ...util.error import BackhaulError
from ...util.log import Log

_log = Log('ui.scenes.register')
LOADED_SCENES = {}

def scene(cls):
	key = cls._id
	_log.debug('Adding Scene %s'%key)
	if key in LOADED_SCENES:
		raise BackhaulError('Scene id %s has already been registered!'%key)
	LOADED_SCENES[key] =  cls
	return cls

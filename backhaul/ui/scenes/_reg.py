from ...util.error import BackhaulError

LOADED_SCENES = {}

def scene(cls):
	key = cls._id
	print('Adding Scene %s'%key)
	if key in LOADED_SCENES:
		raise BackhaulError('Scene id %s has already been registered!'%key)
	LOADED_SCENES[key] =  cls
	return cls

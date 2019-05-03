from collections import OrderedDict
import pyglet
from ...util.error import BackhaulError
from ...types.ui import Sprite
from ...constants import SpriteFrames
from pathlib import PosixPath
from ...util.conf import config

LOADED_TERRAIN = OrderedDict()

def load_texture(base, frame, ext):
	name = '%s-%s.%s'%(base_name, frame, ext)
	texture = pyglet.resource.image(name)


def add_terrain(cls):
	key = cls.__terrain_id__
	if key in LOADED_TERRAIN:
		raise BackhaulError('Terrain id %s already exists!'%key)
	base_name = cls.__base_texture_path__
	if base_name is None:
		if key == 'AIR':
			LOADED_TERRAIN[key] = cls
			return cls
		raise BackhaulError('Terrain %s defines no texture!'%key)

	textures = []
	for frame in SpriteFrames:
		name = '%s-%s.%s'%(base_name, frame.value, cls.__texture_extension__)
		texture = pyglet.resource.image(name)
		textures.append(texture)
	cls.texture = Sprite(*textures)
	LOADED_TERRAIN[key] = cls
	return cls





def get_terrain(id):
	print(LOADED_TERRAIN)
	return LOADED_TERRAIN.get(id)

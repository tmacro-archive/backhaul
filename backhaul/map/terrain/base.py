import pyglet
from ...util.log import Log
from ...constants import SpriteFrames
_log = Log('map.terrain.base')

class BaseTerrain():
	'''
	Base terrain class
	All terrains should subclasses this.
	__base_texture_path__ and __terrain__id should be defined on all child classes
	__base_texture_path__ should contain a base file name/relative filepath to loadable textures found within a pyglet resource path. This will be used to create the various sprites for a given terrain
	__terrain_id__ should contain a unique string that will be usd to identify this terrain via terrain.id.TEXTURE_ID
	'''

	__terrain_id__ = None
	__base_texture_path = None
	__texture_extension__ = 'png'
	__texture_frames = tuple(f.value for f in SpriteFrames)

	def __init__(self, position = None):
		if position is None:
			raise BackhaulError
		self.position = position

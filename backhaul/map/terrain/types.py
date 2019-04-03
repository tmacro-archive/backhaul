from .reg import add_terrain
from .base import BaseTerrain

@add_terrain
class Grass(BaseTerrain):
    __terrain_id__ = 'GRASS'
    __base_texture_path__ = 'grass'

@add_terrain
class Air(BaseTerrain):
	__terrain_id__ = 'AIR'
	__base_texture_path__ = None

@add_terrain
class Dirt(BaseTerrain):
    __terrain_id__ = 'DIRT'
    __base_texture_path__ = 'dirt'

@add_terrain
class Stone(BaseTerrain):
    __terrain_id__ = 'STONE'
    __base_texture_path__ = 'stone'

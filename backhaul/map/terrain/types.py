from .reg import add_terrain
from .base import BaseTerrain

@add_terrain
class Grass(BaseTerrain):
    __terrain_id__ = 'GRASS'
    __texture_path__ = 'grass.png'

@add_terrain
class Dirt(BaseTerrain):
    __terrain_id__ = 'DIRT'
    __texture_path__ = 'dirt.png'

@add_terrain
class Stone(BaseTerrain):
    __terrain_id__ = 'STONE'
    __texture_path__ = 'stone.png'
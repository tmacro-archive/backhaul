from .types import *
from .reg import LOADED_TERRAIN
from collections import namedtuple

id_type = namedtuple('TerrainIds', list(LOADED_TERRAIN.keys()))
id = id_type(**LOADED_TERRAIN)

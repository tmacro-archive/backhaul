from collections import OrderedDict
import pyglet
from ...util.error import BackhaulError

LOADED_TERRAIN = OrderedDict()

def add_terrain(cls):
    key = cls.__terrain_id__
    if key in LOADED_TERRAIN:
        raise BackhaulError('Terrain id %s already exists!'%key)
    tex_path = cls.__texture_path__
    if tex_path is None:
        raise BackhaulError('Terrain %s defines no texture!'%key)
    tex = resolve_texture(tex_path)
    cls.texture = tex if tex else None
    LOADED_TERRAIN[key] = cls
    return cls


def resolve_texture(path):
    return pyglet.resource.image(path)
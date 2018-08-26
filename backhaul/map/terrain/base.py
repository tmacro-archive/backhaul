import pyglet
from ...util.log import Log

_log = Log('map.terrain.base')

class BaseTerrain():
    '''
    Base terrain class
    All terrains should subclasses this.
    __texture_path__ and __terrain__id should be defined on all child classes
    __texture_path__ should contain a file name/relative filepath to a loadable texture found within a pyglet resource path
    __terrain_id__ should contain a unique string that will be usd to identify this terrain via terrain.id.TEXTURE_ID
    '''
    
    __terrain_id__ = None
    __texture_path = None

    def __init__(self, position = None):
        if position is None:
            raise BackhaulError
        self.position = position
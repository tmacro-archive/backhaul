from collections import namedtuple
from ..constants import SpriteFrames


Sprite = namedtuple('Sprite', [f.value for f in SpriteFrames])

# Texture = namedtuple('Texture', 'texture', 'anchor')
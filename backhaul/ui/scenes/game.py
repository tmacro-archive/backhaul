from ..scene import Scene
from ._reg import scene
from ..components.map import Map


@scene
class Game(Scene):
	_id = 'GAME'

	@classmethod
	def build(cls):
		container = glooey.Stack()
		container.alignment = 'fill'
		world_map = Map()

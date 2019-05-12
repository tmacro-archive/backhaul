import glooey
from ._reg import scene
from ..components.common import Text
from ...constants import UIScenes
from ...world.state import World
from .base import Scene

@scene
class Loading(Scene):
	_id = UIScenes.LOADING

	@classmethod
	def handlers(cls):
		return {
			'map:create': cls.on_map_create,
			'map:finish': cls.on_map_finish
		}

	@classmethod
	def build(cls, ui):
		container = glooey.VBox(0)
		container.alignment = 'center'

		title = Text("Loading Map")
		container.add(title)
		return container

	@staticmethod
	def on_map_create(ui, config):
		ui.show_scene(UIScenes.LOADING)
		world = World(config)
		world.build('1337H4CK5', cb=ui.lazy_emit('map:finish', world))

	@staticmethod
	def on_map_finish(ui, world):
		ui.emit('game:start', world)

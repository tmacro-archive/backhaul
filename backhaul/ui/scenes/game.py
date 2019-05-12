from .base import Scene
from ._reg import scene
from ..components.map import Map, MapContainer
from ...constants import UIScenes

@scene
class Game(Scene):
	_id = UIScenes.GAMEHUD

	@classmethod
	def handlers(cls):
		return {
			'game:start': cls.on_game_start
		}

	@classmethod
	def build(cls, ui):
		container = MapContainer()
		world_map = Map()
		container.add(world_map)
		container.set_map(world_map)
		return container

	@staticmethod
	def on_game_start(ui, world):
		widget = ui.get_scene(UIScenes.GAMEHUD)
		map_widget = widget.get_map()
		map_widget.set_map(world.map)
		map_widget.refresh_buffer()
		ui.show_scene(UIScenes.GAMEHUD)

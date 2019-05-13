from .base import Scene
from ._reg import scene
from ..components.common import Text
import glooey
from ...world.state import World, WorldConfig
from functools import partial
from ...constants import UIScenes
from ..components.common import Button
from ...datastore import BackhaulDatastore

@scene
class NewGame(Scene):
	_id = UIScenes.NEWGAME

	@classmethod
	def handlers(cls):
		return {
			'game:new': cls.on_new_game,
			'game:create': cls.on_start_game
		}

	@classmethod
	def build(cls, ui):
		container = glooey.VBox(0)
		container.alignment = 'center'

		title = Text("Creating Map")
		container.add(title)

		button = Button('Start Game')
		button.push_handlers(on_click=ui.lazy_emit('game:create'))
		container.add(button)

		return container

	@staticmethod
	def on_new_game(ui, *args):
		ui.show_scene(UIScenes.NEWGAME)

	@staticmethod
	def on_start_game(ui, *args):
		game = ui.client.create_game('test_game')
		game_conf = WorldConfig.new()
		ui.emit('map:create', game, game_conf)

	@staticmethod
	def on_show(ui):
		ui.emit('game:create')

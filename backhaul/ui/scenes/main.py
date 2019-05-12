from .base import Scene
from ..components.common import Button
from ..components.main import TitleText
import glooey
from ._reg import scene
from functools import partial
from ...world.state import World, WorldConfig
from ...constants import UIScenes


@scene
class MainMenu(Scene):
	_id = UIScenes.MAINMENU

	@classmethod
	def build(cls, ui):
		# Create our outer container
		container = glooey.VBox(0)
		container.alignment = 'center'
		container.cell_padding = 40

		# Create the title
		title = TitleText('Backhaul')
		container.add(title)

		# Create our buttons
		buttons = {
			'New Game':ui.lazy_emit('game:new'),
			'Continue Game':ui.lazy_emit('game:load'),
			'Seed Explorer':ui.lazy_emit('game:seedexplorer'),
			'Settings':ui.lazy_emit('game:settings'),
		} 
		for label, action in buttons.items():
			button = Button(label)
			button.push_handlers(on_click=action)
			container.add(button)

		return container

	@staticmethod
	def on_show(ui):
		ui.emit('game:new')

from ..scene import Scene
from ..components.common import Button
from ..components.main import TitleText
import glooey
from ._reg import scene

@scene
class MainMenu(Scene):
	_id = 'MAIN_MENU'

	@classmethod
	def build(cls):
		# Create our outer container
		container = glooey.VBox(0)
		container.alignment = 'center'
		container.cell_padding = 40

		# Create the title
		title = TitleText('Backhaul')
		container.add(title)

		# Create our buttons
		for label in [
			'New Game',
			'Continue Game',
			'Seed Explorer',
			'Settings'
		]:
			button = Button(label)
			container.add(button)

		return container

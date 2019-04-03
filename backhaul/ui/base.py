import pyglet
from ..util.conf import config
from pathlib import PosixPath
# from .components.title import Title
# from .components.common import Button
import glooey
from .components.base import MainFrame
# from .scenes.main import
# assets = getattr(config, 'assets', None)
# if assets is not None:
# 	_log.debug('Initializing resource paths')
# 	_log.debug(assets)
# 	pyglet.resource.path = assets[:]
# 	pyglet.resource.reindex()
# else:
# 	_log.warning('No asset paths defined!')

class BackhaulUI:
	def __init__(self, resolution, fullscreen):
		self._resolution = resolution
		self._fullscreen = fullscreen
		self.__window = None

	@property
	def _window(self):
		if self.__window is None:
			width, height, _ = self._resolution
			self.__window = pyglet.window.Window(width=width, height=height, fullscreen=self._fullscreen)
		return self.__window

	def _load_assets(self):
		print([p.resolve().as_posix() for p in config.assets])
		pyglet.resource.path = [p.resolve().as_posix() for p in config.assets]
		pyglet.resource.reindex()

	def _load_fonts(self):
		font_path = config.assets.fonts / 'Acme 5 Compressed Caps Outline.ttf'
		font_path = config.assets.fonts / 'PressStart2P-Regular.ttf'
		pyglet.font.add_file(font_path.resolve().as_posix())
		pyglet.font.load('Pess Start 2P')


	def _build_ui(self):
		from .components.title import TitleText, TitleFrame
		from .components.common import Button, MainBox
		self._gui = glooey.Gui(self._window)


		self._gui.add(vbox)



	def _build_game(self):
		pass


	def init(self):
		self._load_assets()
		self._load_fonts()
		self._build_ui()



class UI:
	def __init__(self, initial_scene, scenes):
		self.__window = None
		self.__gui = None
		self.__frame = None
		self.__stage = None
		self._initial_scene = initial_scene
		self.__scenes = scenes

	@property
	def _scenes(self):
		return {
			n: s.build() for n, s in self.__scenes.items()
		}

	@property
	def _window(self):
		if self.__window is None:
			width, height, _ = self._resolution
			self.__window = pyglet.window.Window(width=width, height=height, fullscreen=self._fullscreen)
		return self.__window

	@property
	def _gui(self):
		if self.__gui is None:
			self.__gui = glooey.Gui(self._window)
		return self.__gui

	@property
	def _frame(self):
		if self.__frame is None:
			self.__frame = MainFrame()
			self._gui.add(self.__frame)
		return self.__frame

	@property
	def _stage(self):
		if self.__stage is None:
			self.__stage = glooey.Deck(self._initial_scene, **self._scenes)
			self._frame.add(self.__stage)
		return self.__stage

	def add_scene(self, name, scene):
		return self._stage.add_state(name, scene)

	def get_scene(self, name):
		return self._stage.get_widget(name)

	@property
	def current_scene(self):
		return self._stage.get_state()

	def show_scene(self, name):
		self._stage.set_state(name)

	def show(self, resolution, fullscreen=False):
		self._resolution = resolution
		self._fullscreen = fullscreen
		return self.current_scene

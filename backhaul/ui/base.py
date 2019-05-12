import pyglet
import glooey
from .components.base import MainFrame
from .event import EventEmitter
from itertools import chain

class UI(EventEmitter):
	def __init__(self, initial_scene, scenes):
		super().__init__()
		self.__window = None
		self.__gui = None
		self.__frame = None
		self.__stage = None
		self._initial_scene = initial_scene
		print(initial_scene.value)
		self.__scenes = scenes

	def _build_scene(self, scene):
		handlers = scene.handlers()
		print(handlers)
		self.register(**handlers)
		return scene.build(self)

	@property
	def _scenes(self):
		if self.__scenes is None:
			handler_types = list(chain(list(s.handlers.keys()) for s in self.__scenes.values()))
			for htype in handler_types:
				self.register_event_type(htype)
		return {
			n.value: self._build_scene(s) for n, s in self.__scenes.items()
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
			self.__stage = glooey.Deck(self._initial_scene.value, **self._scenes)
			self._frame.add(self.__stage)
		return self.__stage

	def add_scene(self, name, scene):
		return self._stage.add_state(name, scene)

	def get_scene(self, name=None):
		if name is None:
			name = self.current_scene
		else:
			name = name.value
		return self._stage.get_widget(name)

	@property
	def current_scene(self):
		return self._stage.get_state()

	def show_scene(self, name):
		self._stage.set_state(name.value)
		scene = self.__scenes.get(name)
		if scene and hasattr(scene, 'on_show'):
			scene.on_show(self)

	def show(self, resolution, fullscreen=False):
		self._resolution = resolution
		self._fullscreen = fullscreen
		scene = self.get_scene()
		if scene and hasattr(scene, 'on_show'):
			scene.on_show(self)
		return self.current_scene
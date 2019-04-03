import glooey

class Scene:
	@property
	@classmethod
	def container(cls):
		return glooey.Bin()

	@classmethod
	def build(cls):
		pass

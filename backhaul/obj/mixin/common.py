import uuid
from .._reg import mixin
from ..base import BaseMixin

@mixin
class IdMixin:
	name = 'id'
	can_get = True
	can_set = True
	named = True

	def __init__(self, *args, id = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.id = id

@mixin
class PositionMixin:
	name = 'position'
	can_get = True
	can_set = False
	named = True

	def __init__(self, *args, position=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.position = position

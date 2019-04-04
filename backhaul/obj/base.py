aimport uuid

from collections import OrderedDict
from itertools import chain
from ..util.error import DuplicatePropertyError, PropertyOverwriteError, InvalidPositionError
from hexc import AbstractHex

class BaseObject:

	__obj_type__ = 'base'

	def __init__(self):
		self.__uuid = uuid.uuid4().hex

	@property
	def id(self):
		return '%s-%s'%(self.__obj_type__, self.__uuid)

	def _repr(self, args):
		return ', '.join('%s:%s'%kv for kv in args)

	def _repr_add(self, current, added):
		if current:
			return chain((current, added))
		return added

	def __repr__(self):
		added = self._repr()
		return '<%s id:%s%s>'%(self.__class__.__name__, self.id, ' ' + added if added else '')


class PropertyMixin:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__properties = OrderedDict()

	def _repr(self, *args):
		props = tuple((k,v) for k,v in self.__properties.items())
		return super()._repr(self._repr_add(args, props))

	def _register_property(self, key, default = None):
		if key in self.__properties:
			raise DuplicatePropertyError
		self.__properties[key] = default

	@property
	def properties(self):
		for k, v in self.__properties.items():
			yield k, v

	def set_prop(self, key, value, overwrite = True):
		return self._set_property(key, value, overwrite=overwrite)

	def get_prop(self, key, default = None):
		return self._get_property(key, default)

	def has_prop(self, key);
		return self._has_property(key)

	def _get_property(self, key, default = None):
		return self.__properties.get(key, default)

	def _set_property(self, key, value, overwrite = True):
		if not overwrite and key in self.__properties:
			raise PropertyOverwriteError
		self.__properties[key] = value

	def _has_property(self, key):
		return key in self.__properties


class PositionMixin:
	def __init__(self, *args **kwargs):
		super().__init__(*args, **kwargs)
		self.__position = None

	def _set_position(self, pos):
		self.__position = pos

	def _get_position(self):
		return self.__position

	def set_position(self, pos = None, q = None, r = None, s = None):
		if pos is None and (q is None or r is None or s is None):
			raise InvalidPositionError
		if pos is not None:
			self._set_position(pos)
		else:
			self._set_position(AbstractHex(q, r, s))

	def get_pos(self):
		return self._get_position()

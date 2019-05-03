import inspect, re
from collections import defaultdict
from functools import partialmethod

# Subclasses will set an attribute in the format _attr_{name}
# A property with correctly mapped getters/setters with be created on the class
# If no get/set are found no property is created
# Two class attributes will be set based upon getters/setters found during add
# _attr__get
# _attr__set

BASE_ATTR_TMPL = '_attr_%s '
BASE_ATTR_GET_TMPL = '_attr__%s__get'
BASE_ATTR_SET_TMPL = '_attr__%s__set'
BASE_ATTR_IDX_TMPL = '_attr__%s__idx'
BASE_ATTR_MAP_TMPL = '_attr__%s__map'

OBJECT_TYPES = {}


class BaseEntity:

	def __init__(*args, **kwargs):
		self.__attrs = dict()

	def _has_attr(self, name):
		return hasattr(self, BASE_ATTR_TMPL.format(name=name))

	def _can_get_attr(self, name):
		return hasattr(self, BASE_ATTR_GET_TMPL.format(name=name))

	def _can_set_attr(self, name):
		return hasattr(self, BASE_ATTR_SET_TMPL.format(name=name))

	def _get_attr_(self, name, default=None):
		return self.__attrs.get(name, default)

	def _set_attr(self, name, value):
		self.__attrs[name] = value

class BaseMixin:
	can_get = False # {bool} whether the create a getter
	can_set = False # {bool} whether the create a setter

	index = False # Whether to maintain a list of objects with this attr
	named = False # Maintain a mapping of all objects, keyed with this attributes value. Implies _index


def mixin(cls):
	_property = type('property', (property,), {})
	if not hasattr(cls, '__class__'):
		raise TypeError('@mixin can only be used with new-style classes')

	accessors = defaultdict(dict)
	expected_num_args = {'get': 0, 'set': 1, 'del': 0}
	rewrite_fmt = {
		'get': '_get_attr_%s',
		'set': '_set_attr_%s',
		'del': '_del_attr_%s',
	}

	# The accessors we're searching for are considered methods in python2
	# and functions in python3.  They behave the same either way.
	ismethod = lambda x: inspect.ismethod(x) or inspect.isfunction(x)

	for method_name, method in inspect.getmembers(cls, ismethod):
		accessor_match = re.match('(get|set|del)_(.+)', method_name)
		if not accessor_match:
			continue

		# Suppress a warning by using getfullargspec() if it's available
		# and getargspec() if it's not.
		try: from inspect import getfullargspec as getargspec
		except ImportError: from inspect import getargspec

		prefix, name = accessor_match.groups()
		arg_spec = getargspec(method)
		num_args = len(arg_spec.args) - len(arg_spec.defaults or ())
		num_args_minus_self = num_args - 1

		if num_args_minus_self != expected_num_args[prefix]:
			continue

		accessors[name][prefix] = method

	for name in accessors:
		# Auto create setters and getters if told to
		if getattr(cls, 'can_get', False) and 'get' not in accessors[name]:
			def _getter(self, attr):
				return self._get_attr_(attr)
			_get_mthd = partialmethod(_getter, name)
			setattr(cls, 'get_%s'%name, _get_mthd)
			accessors[name]['get'] = _get_mthd
			delattr(cls, 'can_get')

		if getattr(cls, 'can_set', False) and 'set' not in accessors[name]:
			def _setter(self, attr, value):
				return self._set_attr_(attr, value)
			_set_mthd = partialmethod(_setter, name)
			setattr(cls, 'set_%s'%name, _set_mthd)
			accessors[name]['set'] = _set_mthd
			delattr(cls, 'can_set')

		# Create our property
		setattr(cls, name, _property(
			accessors[name].get('get'),
			accessors[name].get('set'),
			accessors[name].get('del'),
		))
		# Rewrite function names to something that won't clash
		for op, mthd in accessors[name].items():
			setattr(cls, rewrite_fmt[op]%name, mthd) # Add new method
			delattr(cls, '%s_%s'%(op, name)) # Remove old method

		# Set flag for attr existence
		setattr(cls, BASE_ATTR_TMPL%name, True)

		# Set flags for set/get abilities
		if accessors[name].get('get'): # If we can get
			setattr(cls, BASE_ATTR_GET_TMPL%name, True)
		if accessors[name].get('set'): # If we can set
			setattr(cls, BASE_ATTR_SET_TMPL%name, True)

		# Rewrite index/map flags
		setattr(cls, BASE_ATTR_IDX_TMPL%name, getattr(cls, 'index', False))
		setattr(cls, BASE_ATTR_MAP_TMPL%name, getattr(cls, 'named', False))
	return cls

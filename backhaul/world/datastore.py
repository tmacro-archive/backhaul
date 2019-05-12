


class Datastore:
	def __init__(self):
		self._data = {}

	def get(self, key, default=None):
		return self._data.get(key, default)

	def set(self, key, value):
		self.[key] = value

	def del(self, key):
		self._data.pop(key, None)

	def keys(self):
		return self._data.keys()

	def values(self):
		return self._data.values()

	def items(self):
		return self._data.items()




class Datastore:
	def __init__(self, filepath, default_namespace='default'):
		self._path = filepath
		self._default_namespace


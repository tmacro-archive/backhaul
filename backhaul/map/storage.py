

class TerrainMap:
	def __init__(self, size, datastore):
		self.size = size
		self._datastore = datastore

	def get(self, position):
		return self._datastore.get(position)

	def set(self, position, value):
		return self._datastore.set(position, value)

	@property
	def bulk(self):
		return self._datastore.client.atomic
	
	@property
	def model(self):
		return self._datastore.model

	def bulk_set(self, items):
		return self._datastore.bulk_set(items)

	def iter_cube(self, size, center):
		return self._datastore.iter_cube(size, center)
from ..types.grid import Point, add_point, subtr_point, multp_point, div_point
from collections import defaultdict
from functools import partial, partialmethod

class BaseBlock:
	def __init__(self, position):
		self._position = position

	@property
	def position(self):
		return self._position

	@classmethod
	def _new(cls, *args, **kwargs):
		return cls(*args, **kwargs)

	def __add__(self, other):
		return self._new(add_point(self.position, other.position))

	def __sub__(self, other):
		return self._new(subtr_point(self.position, other.position))

	def __matmul__(self, other):
		return self._new(multp_point(self.position, other.position))

	def __floordiv__(self, other):
		return self._new(div_point(self.position, other.position))

class Block(BaseBlock):
	def __init__(self, *args, parent=None):
		self._parent = parent

	def _new(self, *args, **kwargs):
		return super()._new(*args, parent=self.parent, **kwargs)

	@property
	def parent(self):
		return self._parent

	@property
	def value(self):
		return self._parent.get(self.position)

	@value.setter
	def value(self, value):
		return self._parent.set(self._position, value)


class BaseChunk:
	def __init__(self, size, center = Point(0,0,0)):
		self._size = size
		self._center = center

	def _hash(self, position):
		return tuple(position)
		return '{p.x:+}:{p.y:+}:{p.z:+}'.format(p=position)

	@property
	def center(self):
		return self._center

	@property
	def size(self):
		return self._size

	def get(self, position):
		return self._get(self._hash(subtr_point(self._center,position)))

	def set(self, position, value):
		return self._set(self._hash(subtr_point(self._center, position)), value)

	def _get(self, key):
		raise NotImplementedError('_get is not implemented!')

	def _set(self, key, value):
		raise NotImplementedError('_set is not implemented!')

class MemChunk(BaseChunk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._data = dict()

	def _get(self, position):
		return self._data.get(self._hash(position))

	def _set(self, position, value):
		self._data[self._hash(position)] = value
		return True



class BaseChunkLoader:
	def __init__(self, chunk_radius, load_distance, chunk=BaseChunk):
		self._chunk_radius = chunk_radius
		self._chunks = {}
		self._chunk_cls=chunk
		self._load_distance = load_distance

	def _hash(self, position):
		return tuple(position)
		return '{p.x:+}:{p.y:+}:{p.z:+}'.format(p=position)

	def _chunk_lookup(self, position):
		return self._hash(div_point(position, self._chunk_radius))

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self._on_update(value)

	def _on_update(self, position):
		pass

	def chunk(self, position):
		chunk_id = self._chunk_lookup(position)
		return self._chunks.get(chunk_id)

class MemChunkLoader(BaseChunkLoader):
	def __init__(self, *args, chunk=MemChunk, **kwargs):
		super().__init__(*args, chunk=chunk, **kwargs)

	def _new_chunk(self):
		return self._chunk_cls(multp_point(self._chunk_radius, Point(2,2,2)))

	def chunk(self, position):
		chunk_id = self._chunk_lookup(position)
		if chunk_id not in self._chunks:
			self._chunks[chunk_id] = self._new_chunk()
		return self._chunks[chunk_id]


class BaseMap:
	def __init__(self,
		size=Point(500,500,500), # Size of map in blocks
		chunk_radius=Point(250, 250, 250),  # radius * 2 - 1
		load_distance=1,
		loader=BaseChunkLoader,
		block = Block): # Radius of chunks to loads, in chunks

		self._size = size
		self._block = block
		self._loader = loader(chunk_radius, load_distance)
		self._loader.position = Point(0,0,0)

	@property
	def size(self):
		return self._size

	def get(self, position):
		return self._get(position)

	def set(self, position, value):
		return self._set(position, value)

	def block(self, position):
		return self._block(position)

	def _get(self, position):
		chunk = self._loader.chunk(position)
		if chunk:
			return chunk.get(position)

	def _set(self, position, value):
		chunk = self._loader.chunk(position)
		if chunk:
			return chunk.set(position, value)

class MemMap(BaseMap):
	def __init__(self, *args, loader=MemChunkLoader, **kwargs):
		super().__init__(*args, loader=loader, **kwargs)

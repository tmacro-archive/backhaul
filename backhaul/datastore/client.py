import peewee
from playhouse.sqlite_ext import CSqliteExtDatabase
from .layers import build_layers
from ..util.conf import config
from pathlib import PosixPath

class DatastoreClient:
    def __init__(self, filepath):
        self._path = filepath
        self._connection = None
        self._connected = False
        self.__layers = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = CSqliteExtDatabase(
                self._path,
                pragmas=(
                    ('cache_size', -1024 * 64),  # 64MB page-cache.
                    ('journal_mode', 'wal'),  # Use WAL-mode (Write Ahead Log).
                )
            )
        return self._connection
    
    def connect(self):
        if not self._connected:
            db = self.connection
            db.connect()
            self._init_datastore()
            self._load_datastore()
            self._connected = True
        return db

    @property
    def _layers(self):
        if self.__layers is None:
            self.__layers = build_layers(self.connection)
        return self.__layers

    def _init_datastore(self):
        for layer in self._layers:
            try:
                self.connection.create_tables([layer.model], safe=False)
                layer.on_create()
            except peewee.OperationalError:
                pass

    def _load_datastore(self):
        for layer in self._layers:
            layer.on_load()

class BackhaulDatastore:
    def __init__(self):
        self._save_dir = PosiPath(config.data.saved_games).resolve()

    def _get_path(self, name):
        return self._save_dir / name.lower()

    def load(self, name):
        return DatastoreClient(self._get_path(name))

    def delete(self, name):
        pass

    def create(self, name):
        return DatastoreClient(self._get_path(name))
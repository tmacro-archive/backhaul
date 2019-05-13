import peewee
try:
    from playhouse.sqlite_ext import CSqliteExtDatabase as SqliteExtDatabase
except ImportError:
    from playhouse.sqlite_ext import SqliteExtDatabase
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
            self._connection = SqliteExtDatabase(
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
    def layers(self):
        if self.__layers is None:
            self.__layers = build_layers(self.connection)
        return self.__layers

    def _init_datastore(self):
        for layer in self.layers:
            try:
                self.connection.create_tables([layer.model], safe=False)
                layer.on_create()
            except peewee.OperationalError:
                pass

    def _load_datastore(self):
        for layer in self.layers:
            layer.on_load()

class BackhaulDatastore:
    def __init__(self):
        self._save_dir = PosixPath(config.data.saved_games).resolve()

    def _get_path(self, name):
        return self._save_dir / name.lower()

    def load(self, name):
        client = DatastoreClient(self._get_path(name))
        client.connect()
        return client
    def delete(self, name):
        pass

    def create(self, name):
        client = DatastoreClient(self._get_path(name))
        client.connect()
        return client
from peewee import TextField, BlobField
from peewee import Model as BaseModel
import msgpack
import json

class BaseLayer:
    class Model(BaseModel):
        pass

    class Layer:
        model = None
        client = None
        def on_create(self):
            pass

        def on_load(self):
            pass

class KeyValue(BaseLayer):
    class Model(BaseLayer.Model):
        key = TextField(primary_key=True)
        value = TextField()

    class Layer(BaseLayer.Layer):
        def get(self, key):
            val = self.model.get_by_id(key)
            if val:
                return val.value

        def set(self, key, value):
            return self.model.create(key=key, value=value)

        def rem(self, key):
            val = self.model.get_by_id(key)
            if val:
                return val.delete_instance()
            return 0

# Can be mixed with KeyValue to allow MessagePack value serialization
class MessagePackMixin:
    class Model(BaseModel):
        key = TextField(primary_key=True)
        value = BlobField()

    class Layer:
        def get(self, *args, **kwargs):
            return msgpack.unpackb(
                super().get(*args, **kwargs),
                use_list=False, # unpack arrays to tuples instead of list
                raw=False # distinguish between bytes and strings
            )

        def set(self, key, value):
            return super().set(
                key, 
                msgpack.packb(
                    value, 
                    use_bin_type=True # distinguish between bytes and strings
                )
            )

# Can be mixed with KeyValue to allow JSON value serialization
class JSONMixin:
    class Layer:
        def get(self, *args, **kwargs):
            return json.loads(super().get(*args, **kwargs))

        def set(self, key, value):
            return super().set(key, json.dumps(value))

# import sqlite3
# from UserDict import DictMixin as DictClass

# class KeyValueStore(DictClass):
#     def __init__(self, filename=None):
#         self.conn = sqlite3.connect(filename)
#         self.conn.execute("CREATE TABLE IF NOT EXISTS kv (key text unique, value text)")
#         self.c = self.conn.cursor()

#     def close():
#         self.conn.commit()
#         self.conn.close()

#     def __len__(self):
#         self.c.execute('SELECT COUNT(*) FROM kv')
#         rows = self.c.fetchone()[0]
#         return rows if rows is not None else 0

#     def iterkeys(self):
#         c1 = self.conn.cursor()
#         for row in c1.execute('SELECT key FROM kv'):
#             yield row[0]

#     def itervalues(self):
#         c2 = self.conn.cursor()
#         for row in c2.execute('SELECT value FROM kv'):
#             yield row[0]

#     def iteritems(self):
#         c3 = self.conn.cursor()
#         for row in c3.execute('SELECT key, value FROM kv'):
#             yield row[0], row[1]

#     def keys(self):
#         return list(self.iterkeys())

#     def values(self):
#         return list(self.itervalues())

#     def items(self):
#         return list(self.iteritems())

#     def __contains__(self, key):
#         self.c.execute('SELECT 1 FROM kv WHERE key = ?', (key,))
#         return self.c.fetchone() is not None

#     def __getitem__(self, key):
#         self.c.execute('SELECT value FROM kv WHERE key = ?', (key,))
#         item = self.c.fetchone()
#         if item is None:
#             raise KeyError(key)
#         return item[0]

#     def __setitem__(self, key, value):
#         self.c.execute('REPLACE INTO kv (key, value) VALUES (?,?)', (key, value))
#         self.conn.commit()

#     def __delitem__(self, key):
#         if key not in self:
#             raise KeyError(key)
#         self.c.execute('DELETE FROM kv WHERE key = ?', (key,))
#         self.conn.commit()

#     def __iter__(self):
#         return self.iteritems()
from collections import namedtuple
from peewee import Model

LAYERS = {}

def layer(cls):
    LAYERS[cls.__name__.lower()] = cls


def make_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + '_tbl'

def build_layers(db):
    built_layers = {}
    class metacls:
        database = db
        table_function = lambda m: m._table_name
    for name, layer in LAYERS.items():
        class modelcls(layer.Model):
            Meta = metacls
            _table_name = name
        class layercls(layer.Layer):
            model = modelcls
            client = db
        built_layers[name] = layercls()
    _layers = namedtuple('layers', list(sorted(built_layers.keys())))
    return _layers(**built_layers)
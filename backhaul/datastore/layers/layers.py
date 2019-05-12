from ._reg import layer
from .base import KeyValue, JSONMixin, BaseLayer
from ...util.conf import config
from datetime import datetime
from peewee import IntegerField




@layer
class Meta(KeyValue):
    class Layer(JSONMixin.Layer, KeyValue.Layer):
        def on_create(self):
            self.set('game_version', config.meta.version)
            self.set('created', datetime.utcnow().isoformat())
            self.set('format_version', 1)

        @property
        def game_version(self):
            return self.get('game_version')

        @property
        def created(self):
            return datetime.fromisoformat(self.get('created'))

        @property
        def format_version(self):
            return self.get('format_version')

@layer
class Terrain(BaseLayer):
    class Model(BaseLayer.Model):
        x = IntegerField()
        y = IntegerField()
        z = IntegerField()
        terrain_type = IntegerField()

    class Layer(BaseLayer.Layer):
        def get(self, position):
            try:
                return self.model.get(
                    self.model.x == position.x,
                    self.model.y == position.y,
                    self.model.z == position.z
                ).terrain_type
            except self.model.DoesNotExist:
                return None
        
        def set(self, position, terrain_type):
            val =self.model.select().where((self.model.x == position.x) & (self.model.y == position.y) & (self.model.z == position.z)).first()
            if val:
                val.terrain_type = terrain_type
                val.save()
            else:
                self.model.create(terrain_type=terrain_type, **position._asdict())
        
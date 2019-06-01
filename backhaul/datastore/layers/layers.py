from ._reg import layer
from .base import KeyValue, JSONMixin, BaseLayer
from ...util.conf import config
from datetime import datetime
from peewee import IntegerField, TextField
from ...map.terrain import get_terrain
from ...util.iter import chunked


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
        terrain_type = TextField()

    class Layer(BaseLayer.Layer):
        def get(self, position):
            try:
                terrain = self.model.get(
                    self.model.x == position.x,
                    self.model.y == position.y,
                    self.model.z == position.z
                ).terrain_type
                print(terrain)
                return get_terrain(terrain)
            except self.model.DoesNotExist:
                print('eeeee')
                return None
        
        def set(self, position, terrain_type):
            val =self.model.select().where((self.model.x == position.x) & (self.model.y == position.y) & (self.model.z == position.z)).first()
            if val:
                val.terrain_type = terrain_type.__terrain_id__
                val.save()
            else:
                self.model.create(terrain_type=terrain_type.__terrain_id__, **position._asdict())
        
        def bulk_set(self, items):
            with self.client.atomic():
                for chunk in chunked(items, 500):
                    self.model.insert_many(
                        [{
                            'x': i[0].x,
                            'y': i[0].y,
                            'z': i[0].z,
                            'terrain_type':i[1]
                        } for i in chunk]
                    ).execute()

        def iter_cube(self, size, center):
            x_range = center_range(size.x, center.x)
            y_range = center_range(size.y, center.y)
            z_range = center_range(size.z, center.z)
            return self.model.select().where(
                (self.model.x >= x_range[0]) & (self.model.x < x_range[0]) &
                (self.model.y >= y_range[0]) & (self.model.y < y_range[0]) &
                (self.model.z >= z_range[0]) & (self.model.z < z_range[0])
            ).execute()

        # def iter_cube_screen(self, size, center):
        #     x_range = center_range(size.x, center.x)
        #     y_range = center_range(size.y, center.y)
        #     z_range = center_range(size.z, center.z)
        #     return self.model.select().where(
        #         self.model.x.between(*x_range),
        #         self.model.y.between(*y_range),
        #         self.model.z.between(*z_range),
        #     ).order_by(
        #         self.model.x
        #         self.model.y
        #         self.model.z
        #     )
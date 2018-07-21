from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from zope.interface import Interface
from guillotina.schema import JSONField

import json


LAYOUT_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'cols': {'type': 'array'}
    },
})

DATA_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'blocks': {'type': 'array'}
    },
})


class ITiles(Interface):
    tiles_layout = JSONField(
        title='Layout of the block',
        schema=LAYOUT_SCHEMA)

    tiles = JSONField(
        title='Data of the block',
        schema=DATA_SCHEMA)


@configure.behavior(
    title="Tiles behavior",
    provides=ITiles,
    for_="guillotina.interfaces.IResource")
class Tiles(AnnotationBehavior):
    __annotations_data_key__ = 'itiles'
    

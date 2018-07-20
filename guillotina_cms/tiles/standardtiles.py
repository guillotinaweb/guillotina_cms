from guillotina import configure
from guillotina import schema

from zope.interface import Interface
from . import tile


# Titol
# Descripcio
# Text
# image
# video
tile(
    name='title', title='title', schema=ITileTitle
)
class ITileTitle(Interface):
    title = schema.TextLine(required=True)


class ITileDescription(Interface)
    text = schema.TextLine(required=True)



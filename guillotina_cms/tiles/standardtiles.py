from guillotina import configure
from guillotina import schema

from zope.interface import Interface
from guillotina_cms import configure_cms


# Titol
# Descripcio
# Text
# image
# video
@configure_cms.tile(
    name='title', title='title'
)
class ITileTitle(Interface):
    title = schema.TextLine(required=True)


# class ITileDescription(Interface):
#     text = schema.TextLine(required=True)




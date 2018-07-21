
from guillotina import configure
from guillotina import schema
from guillotina_cms import configure_cms
from zope.interface import Interface


@configure_cms.tile(
    name='title', title='title'
)
class ITileTitle(Interface):
    title = schema.TextLine(required=True)


# class ITileDescription(Interface):
#     text = schema.TextLine(required=True)
# Titol
# Descripcio
# Text
# image
# video



from zope.interface import Interface
from guillotina.schema.interfaces import IObject
from guillotina import schema


class ICMSLayer(Interface):
    """Marker interface layer Plone.CMS."""


class IRichTextField(IObject):
    """Rich text field"""


class IRichTextFieldSchema(Interface):
    """Rich text field schema"""
    content_type = schema.ASCII(
        title='Content type'
    )
    data = schema.Text(
        title='Real data'
    )
    encoding = schema.ASCII(
        title='Get the real encoding'
    )


# Components for REST API


class IObjectWorkflow(Interface):
    pass


class ITileType(Interface):
    """A utility that describes a type of tile
    """

    __name__ = schema.DottedName(
        title='Tile name (same as utility name)'
    )

    title = schema.TextLine(title=u'Title')

    description = schema.Text(title=u'Description', required=False)

    icon = schema.Text(title=u'Icon', required=False)

    add_permission = schema.Id(title=u'Zope 3 IPermission utility name')

    schema = schema.Object(
        title=u'Tile schema',
        description=u'Describes configurable data for this tile and allows a '
                    u'form to be rendered to edit it. Set to None if the tile '
                    u'has no configurable schema',
        schema=Interface,
        required=False,
    )

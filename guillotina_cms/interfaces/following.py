from zope.interface import Interface
from guillotina import schema
from guillotina.directives import index_field
from guillotina.directives import read_permission
from guillotina.directives import write_permission
from guillotina_cms.directives import hidden_field


class IMarkerFollowing(Interface):
    """Marker interface for following."""


class IFollowing(Interface):
    hidden_field('favorites')
    hidden_field('favorite')

    index_field('favorites', type='keyword', store=True)

    read_permission(favorites='guillotina.')
    write_permission(favorites='guillotina.NoBody')
    favorites = schema.List(
        title=u'favorites',
        default=[],
        value_type=schema.TextLine(title='follower'))

    favorite = schema.Bool(
        title=u'Current user has it favorited',
        default=False)
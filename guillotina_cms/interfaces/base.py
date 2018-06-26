from zope.interface import Interface
from guillotina import schema


class ICMSLayer(Interface):
    """Marker interface layer Plone.CMS."""


class ICMSBehavior(Interface):

    hidden_navigation = schema.Bool(
        title='Should be hidden on navigation',
        default=False)

    language = schema.Choice(
        title='Language')

    review_state = schema.Choice(
        title='Workflow review state')
